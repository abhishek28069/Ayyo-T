const express = require("express");
const axios = require("axios");
const cors = require("cors");
const app = express();
const bodyParser = require("body-parser");
app.use(bodyParser.json());
app.use(cors());

app.route("/sensor/types").get(async (req, res) => {
  axios
    .get("https://iudx-rs-onem2m.iiit.ac.in/resource/sensors")
    .then((response) => {
      let data = response.data;
      let keys = Object.keys(data);
      console.log(keys);
      response = { data: keys };
      res.json(response);
    })
    .catch((error) => {
      console.error(error);
    });
});

app.route("/sensor/type/nodes/:sensor_type").get(async (req, res) => {
  // const sensor_type = req.body.sensor_type;
  const sensor_type = req.params.sensor_type;
  console.log(`🥶 ${sensor_type}`);
  axios
    .get("https://iudx-rs-onem2m.iiit.ac.in/resource/nodes/")
    .then((response) => {
      let data = response.data;
      console.log("sdas");
      data = data["results"];
      let result_set = [];
      let count = 0;

      for (const key in data) {
        // console.log(`${key}`)
        nodes = data[key];
        const myset = new Set(nodes);
        // console.log(myset.size)
        result_set.push(...nodes);
      }
      // console.log(result_set.length)
      result_set = new Set(result_set);
      result_set = Array.from(result_set);
      // console.log(result_set)
      const result = { data: result_set };
      res.json(result);
    })
    .catch((err) => {});
  console.log(sensor_type);
});

app.route("/sensor/data/:node_id").get(async (req, res) => {
  // const node_id = req.body.node_id;
  const node_id = req.params.node_id;
  // console.log(req.body.hi)
  console.log(node_id);
  axios
    .get(`https://iudx-rs-onem2m.iiit.ac.in/channels/${node_id}/feeds`)
    .then((response) => {
      let data = response.data["feeds"][0];
      let signature = response.data["channel"];
      const result = {
        signature: signature,
        data: data,
      };
      console.log("data", result);
      res.json(result);
    })
    .catch((err) => {});
});

app.listen(3000, function () {
  console.log("Server started on port 3000");
});
