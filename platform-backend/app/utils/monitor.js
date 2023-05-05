const Kafka = require("node-rdkafka");

function startMonitoring() {
  const producer = new Kafka.Producer({
    "metadata.broker.list": "20.75.91.206:9092",
    dr_cb: true,
  });

  function json_serializer(data) {
    return JSON.stringify(data);
  }

  producer.on("ready", function () {
    console.log("Kafka producer is ready");
    setInterval(() => {
      producer.produce("platform_backend_to_monitoring", null, Buffer.from(json_serializer({ message: "scheduler is alive" })), null, Date.now());
      console.log("Sent message to Kafka");
    }, 20000);
  });

  producer.on("delivery-report", function (err, report) {
    if (err) {
      console.error("Failed to deliver message to Kafka:", err);
    } else {
      console.log("Message delivered to Kafka:", report);
    }
  });

  producer.connect();
}

module.exports = { startMonitoring };
