validateJSON = (data) => {
  try {
    const json = JSON.parse(data);
    // Check if all required fields are present
    const requiredFields = ["app_name", "app_description", "cmd", "sensors"];
    const fieldsPresent = requiredFields.every((field) => json.hasOwnProperty(field));
    if (!fieldsPresent) return false;
    // Check if app_name and app_description are strings
    if (typeof json.app_name !== "string" || typeof json.app_description !== "string") {
      return false;
    }
    // Check if cmd is an array of strings
    if (!Array.isArray(json.cmd) || !json.cmd.every((cmd) => typeof cmd === "string")) {
      return false;
    }
    // Check if sensors is an object with only the allowed keys
    const allowedKeys = ["Temperature", "Humidity", "Luminosity", "Power", "Presence", "Lamp", "Buzzer", "AQI", "SL", "EM"];
    const sensorKeys = Object.keys(json.sensors);
    if (!sensorKeys.every((key) => allowedKeys.includes(key))) {
      return false;
    }
    // Check if sensors has string keys and number values
    if (!sensorKeys.every((key) => typeof key === "string" && typeof json.sensors[key] === "number")) {
      return false;
    }
    // All checks passed
    return true;
  } catch (e) {
    return false;
  }
};

module.exports = { validateJSON };
