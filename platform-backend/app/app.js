const express = require("express");
const multer = require("multer");

const { v4: uuidv4 } = require("uuid");
const bodyParser = require("body-parser");
const cors = require("cors");
const ldap = require("ldapjs");
const fetch = require("node-fetch-commonjs");
const Kafka = require("node-rdkafka");
const { createClient } = require("@supabase/supabase-js");
const { validateJSON } = require("./utils/validateJson");
const { startMonitoring } = require("./utils/monitor");

const app = express();
const upload = multer();

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

/* ---------------------------------- URLS ---------------------------------- */
const ldap_base_url = "ldap://openldap:389";
const sensor_query_base_url = "http://sensor_manager:2000";

// Initialize Supabase client
const supabase = createClient(
  "https://btyzbfeqwkepwgobehxw.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0eXpiZmVxd2tlcHdnb2JlaHh3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODE0NjgyOTQsImV4cCI6MTk5NzA0NDI5NH0.FPhB2K8Zw796-3YtiS5yEOvqJEAkICmak-l2RqFB6Mc"
);

const publishMessage = (app_crons) => {
  const producer = new Kafka.Producer({
    "client.id": "kafka-producer",
    "metadata.broker.list": "20.75.91.206:9092", // Replace with your Kafka bootstrap servers
    "api.version.request": true,
    dr_msg_cb: true, // Delivery report callback
  });

  producer.connect();

  producer.on("ready", () => {
    console.log("publishing kafka message-", app_crons);
    producer.produce(
      "scheduled_apps3", // Replace with the name of your Kafka topic
      null,
      new Buffer.from(JSON.stringify(app_crons)),
      null,
      Date.now(),
      (err, report) => {
        if (err) {
          console.error(`Failed to deliver message: ${err}`);
        } else {
          console.log(`Message delivered to topic: ${report.topic}, partition: ${report.partition}, offset: ${report.offset}`);
        }
      },
      // Use JSON.stringify as key serializer
      { keySerializer: (data) => new Buffer.from(JSON.stringify(data)) }
    );
  });

  producer.on("event.error", (err) => {
    console.error(`Producer error: ${err}`);
  });
};

const publishZipFile = async (app_id) => {
  const stream = Kafka.Producer.createWriteStream(
    {
      "metadata.broker.list": "20.75.91.206:9092",
      "message.max.bytes": 20971520,
    },
    {},
    { topic: "app_zips" }
  );
  const { data, error } = await supabase.storage.from("application").download(`${app_id}/app.zip`);
  console.log(data);
  const success = stream.write(Buffer.from(await data.arrayBuffer()), (error) => {
    if (!error) {
      console.log("file sent successfully");
    } else {
      console.log("file failed to send", error);
    }
  });
};

// Login route
app.post("/login", (req, res) => {
  const ldapClient = ldap.createClient({
    url: ldap_base_url,
  });
  const { username, password, role } = req.body;

  ldapClient.bind(`cn=${username}_${role},dc=example,dc=org`, password, (err) => {
    if (err) {
      res.status(401).json("Authentication failed");
    } else {
      res.json("Authentication successful");
    }
  });
});

// Register route
app.post("/register", (req, res) => {
  const ldapClient = ldap.createClient({
    url: ldap_base_url,
  });
  const { username, email, password, role } = req.body;
  ldapClient.bind("cn=admin,dc=example,dc=org", "admin", (err) => {
    if (err) {
      res.status(401).json("LDAP connection failed");
    } else {
      const entry = {
        gn: role,
        mail: email,
        userPassword: password,
        sn: username,
        objectclass: "inetOrgPerson",
      };

      ldapClient.add(`cn=${username}_${role},dc=example,dc=org`, entry, (err) => {
        if (err) {
          res.status(400).json("Registration failed");
        } else {
          res.json("Registration successful");
        }
      });
    }
  });
});

// Delete route
app.delete("/user/:username/role/:role", (req, res) => {
  const ldapClient = ldap.createClient({
    url: ldap_base_url,
  });
  const { username, role } = req.params;

  ldapClient.bind("cn=admin,dc=example,dc=org", "admin", (err) => {
    if (err) {
      res.status(401).json("LDAP connection failed");
    } else {
      ldapClient.del(`cn=${username}_${role},dc=example,dc=org`, (err) => {
        if (err) {
          res.status(400).json("User deletion failed");
        } else {
          res.json("User deleted successfully");
        }
      });
    }
  });
});

// Route to handle file upload
app.post("/upload-files", upload.fields([{ name: "zip" }, { name: "config" }]), async (req, res) => {
  const { zip, config } = req.files;
  const { authUser } = req.body;
  if (!zip || !config) {
    return res.status(400).json({ error: "zip and config files are required" });
  }
  try {
    // Validate JSON
    const isValid = validateJSON(config[0].buffer.toString());
    if (isValid) {
      console.log("The JSON is valid");
      const app_id = uuidv4();
      // Store in applications table
      const { data, error } = await supabase.from("apps").insert([{ username: authUser, app_id }]);
      // Upload in Supabase storage
      const { data: zipData, error: zipError } = await supabase.storage.from("application").upload(`${app_id}/app.zip`, zip[0].buffer, {
        cacheControl: "3600",
        upsert: false,
      });
      const { data: configData, error: configError } = await supabase.storage.from("application").upload(`${app_id}/config.json`, config[0].buffer, {
        cacheControl: "3600",
        upsert: false,
      });
      console.log(zipError, configError);
      return res.status(200).json({ message: "File upload successful" });
    } else {
      console.log("The JSON is not valid");
      return res.status(400).json({ error: "JSON validation failed" });
    }
  } catch (error) {
    console.log("Error uploading file:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/sensor-bindings", async (req, res) => {
  const sensorRequirements = req.body;
  console.log(sensorRequirements);

  fetch(sensor_query_base_url + "/api/list/groups/custom", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(sensorRequirements),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      res.send(data);
    })
    .catch((error) => {
      console.error("Error:", error);
      res.send("error");
    });
});

app.post("/schedule-app", async (req, res) => {
  const { enduser_name, app_id, schedule_info, sensor_binding, location, sched_flag, user_kill, app_name } = req.body;
  try {
    const instance_id = req.body?.instance_id || uuidv4();
    const { data, error } = await supabase
      .from("scheduled_apps")
      .insert([{ location, enduser_name, app_id, instance_id, schedule_info, sensor_bindings: sensor_binding, sched_flag }]);
    if (error) {
      throw error;
    }
    publishMessage({ location, enduser_name, app_id, instance_id, schedule_info, sensor_bindings: sensor_binding, sched_flag, user_kill, app_name });
    // publishZipFile(app_id);
    return res.status(200).json({ message: "App scheduled successfully" });
  } catch (error) {
    console.log("error while inserting row into scheduled_apps table", error);
    return res.status(500).json({ error: "Internal server error" });
  }
});

startMonitoring();

app.listen(3001, () => {
  console.log("Platform Server is running on port 3001");
});
