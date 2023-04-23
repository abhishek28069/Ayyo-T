import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import DBService as DB

onem2m_api_base_url = "http://localhost:8069"

app = Flask(__name__)
CORS(app)


@app.route("/api")
def index():
    return "Hello World"


@app.route("/api/list/groups", methods=["GET"])
def listGroups():
    print("Listing Groups...")
    db_res = dict(DB.getGroups())
    print(f"Response: {db_res}")
    return db_res


@app.route("/api/list/types", methods=["GET"])
def listTypes():
    print("Listing Types...")
    db_res = dict(DB.getTypes())
    print(f"Response: {db_res}")
    return db_res


@app.route("/api/list/sensors", methods=["GET"])
def listSensors():
    group = request.args.get("group")
    type = request.args.get("type")
    activated = request.args.get("activated")
    db_res = ""
    if group is not None and type is not None:
        db_res = DB.getSensorsByGroupAndType(group, type, activated)
    elif group is not None:
        db_res = DB.getSensorsByGroup(group, activated)
    elif type is not None:
        db_res = DB.getSensorsByType(type, activated)
    else:
        db_res = DB.getSensors(activated)
    print(dict(db_res))
    return dict(db_res)


@app.route("/api/sensor/info")
def sensorInfo():
    sensor_name = request.args.get("sensor_name")
    if sensor_name is None:
        return {"error": True, "msg": "Name is required"}
    return DB.getSensorByName(sensor_name)


@app.route("/api/sensor/latestdata")
def getLatestSensorData():
    sensor_id = request.args.get("sensor_id")
    if sensor_id is None:
        return {"error": True, "msg": "Name is required"}
    return DB.getLatestData(sensor_id)


@app.route("/api/sensor/historicdata")
def getHistoricData():
    sensor_id = request.args.get("sensor_id")
    row_count = int(request.args.get("row_count", default=100))
    if sensor_id is None:
        return {"error": True, "msg": "Name is required"}
    return DB.getHistoricData(row_count, sensor_id)


@app.route("/api/trigger")
def trigger():
    # parse query params
    sensor_name = request.args.get("sensor_name")
    trigger = request.args.get("trigger")  # on/off
    # get full sensor info
    sensor = DB.getSensorByName(sensor_name)
    print(type(sensor))
    # get the currwent status (activated/deactivated) and gracefully exit if already in triggered state
    if (sensor["activated"] == False and trigger == "off") or (
        sensor["activated"] == True and trigger == "on"
    ):
        return {"error": False, "msg": "Already in the required state"}
    # make a request to onem2m backend
    url = (
        onem2m_api_base_url + "/rundevicescript"
        if trigger == "on"
        else onem2m_api_base_url + "/stopdevicescript"
    )
    payload = {
        "device_type": sensor["sensor_type"],
        "device_group": sensor["group_name"],
        "device_name": sensor["sensor_name"],
        "container": sensor["sensor_name"] + "_data",
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            return {"error": False, "msg": "success turning " + trigger}
        else:
            return {"error": True, "msg": "failed turning " + trigger}
    except requests.exceptions.RequestException as e:
        print("---------------------------", e)
        return {"error": True, "msg": str(e)}


@app.route("/api/list/groups/custom", methods=["POST"])
def listCustomGroups():
    # Expects request of json type , body in data attribute .
    # data attribute has list of objects each containing sensor_type and count (Types are implicit).
    req_body = request.get_json()
    print(f"Req: {req_body}")
    response = DB.getCustomGroups(req_body["sensors"])
    return response


if __name__ == "__main__":
    app.run(port=2000, debug=True, host="0.0.0.0")
