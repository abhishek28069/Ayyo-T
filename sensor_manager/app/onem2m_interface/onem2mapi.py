import os
import time
import math
import json
import random
import threading
import requests
from subprocess import Popen, PIPE, STDOUT

from flask import Flask, request, jsonify
from flask_cors import CORS

from db import (
    register_sensor,
    delete_sensor_entry,
    delete_sensor_data,
    toggle_sensor,
    is_name_available,
    fetch_sensors,
)


app = Flask(__name__)

CORS(app)


@app.route("/")
def hello():
    return "OneM2M API"


@app.route("/createae", methods=["POST"])
def create_ae():
    request_json = request.get_json()  # Get JSON data from request

    uri_cse = request_json.get("uri_cse")  # Retrieve uri_cse from JSON body
    ae_name = request_json.get("ae_name")
    ae_labels = request_json.get("ae_labels", "")
    data_format = request_json.get("data_format", "json")

    print(uri_cse, ae_labels, ae_name, data_format)

    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{};ty=2".format(data_format),
    }

    body = {
        "m2m:ae": {
            "rn": "{}".format(ae_name),
            "api": "acp_admin",
            "rr": "true",  # resource reachable from CSE
            "lbl": ae_labels,
        }
    }

    try:
        response = requests.post(uri_cse, json=body, headers=headers)
    except TypeError:
        response = requests.post(uri_cse, data=json.dumps(body), headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    return "Success" if response.status_code == 201 else "Error"


@app.route("/createcnt", methods=["POST"])
def create_cnt():
    request_json = request.get_json()  # Get JSON data from request

    uri_ae = request_json.get("uri_ae")  # Retrieve uri_ae from JSON body
    cnt_name = request_json.get("cnt_name")
    cnt_labels = request_json.get("cnt_labels", "")
    data_format = request_json.get("data_format", "json")

    print(uri_ae, cnt_labels, cnt_name, data_format)

    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{};ty=3".format(data_format),
    }

    body = {"m2m:cnt": {"rn": "{}".format(cnt_name), "mni": 120, "lbl": cnt_labels}}

    try:
        response = requests.post(uri_ae, json=body, headers=headers)
    except TypeError:
        response = requests.post(uri_ae, data=json.dumps(body), headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    return "Success" if response.status_code == 201 else "Error"


@app.route("/createdesccin", methods=["POST"])
def create_desc_cin():
    request_json = request.get_json()  # Get JSON data from request

    uri_desc_cnt = request_json.get(
        "uri_desc_cnt"
    )  # Retrieve uri_desc_cnt from JSON body
    node_description = request_json.get("node_description")
    desc_cin_labels = request_json.get("desc_cin_labels", "")
    data_format = request_json.get("data_format", "json")

    print(uri_desc_cnt, desc_cin_labels, node_description, data_format)

    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{};ty=4".format(data_format),
    }

    body = {
        "m2m:cin": {
            "cnf": "application/json",
            "con": node_description,
            "lbl": desc_cin_labels,
        }
    }

    try:
        response = requests.post(uri_desc_cnt, json=body, headers=headers)
    except TypeError:
        response = requests.post(uri_desc_cnt, data=json.dumps(body), headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    return "Success" if response.status_code == 201 else "Error"


@app.route("/createdatacin", methods=["POST"])
def create_data_cin():
    request_json = request.get_json()  # Get JSON data from request

    uri_data_cnt = request_json.get("uri_data_cnt")  # Retrieve uri_cnt from JSON body
    value = request_json.get("value")
    cin_labels = request_json.get("cin_labels", "")
    data_format = request_json.get("data_format", "json")

    print(uri_data_cnt, cin_labels, value, data_format)

    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{};ty=4".format(data_format),
    }

    body = {"m2m:cin": {"con": "{}".format(value), "lbl": cin_labels, "cnf": "text"}}

    try:
        response = requests.post(uri_data_cnt, json=body, headers=headers)
    except TypeError:
        response = requests.post(uri_data_cnt, data=json.dumps(body), headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    return "Success" if response.status_code == 201 else "Error"


@app.route("/creategroup", methods=["POST"])
def create_group():
    request_json = request.get_json()  # Get JSON data from request

    uri_cse = request_json.get("uri_cse")  # Retrieve uri_cse from JSON body
    group_name = request_json.get("group_name")
    uri_list = request_json.get("uri_list")
    data_format = request_json.get("data_format", "json")

    print(uri_cse, group_name, uri_list, data_format)

    headers = {"X-M2M-Origin": "admin:admin", "Content-type": "application/json;ty=9"}

    payload = {"m2m:grp": {"rn": group_name, "mt": 3, "mid": uri_list, "mnm": 10}}

    try:
        response = requests.post(uri_cse, json=payload, headers=headers)
    except TypeError:
        response = requests.post(uri_cse, data=json.dumps(payload), headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    return "Success" if response.status_code == 201 else "Error"


##########################################################################################################


@app.route("/getdata", methods=["GET"])
def get_data():
    uri = request.args.get("uri")
    data_format = request.args.get("data_format", default="json")
    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{}".format(data_format),
    }
    response = requests.get(uri, headers=headers)
    status_code = response.status_code
    response_text = response.text
    _resp = json.loads(response_text)
    return jsonify(
        {
            "status_code": status_code,
            "content": _resp["m2m:cin"][
                "con"
            ]  # To get latest or oldest content instance
            # 'content': _resp["m2m:cnt"]["con"]  # To get whole data of container (all content instances)
        }
    )


def get_group_data(uri, data_format="json"):
    """
    Method description:
    Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
    under the specified CSE

    Parameters:
    uri_cse : [str] URI of parent CSE
    ae_name : [str] name of the AE
    fmt_ex : [str] payload format
    """
    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{}".format(data_format),
    }

    response = requests.get(uri, headers=headers)
    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    _resp = json.loads(response.text)
    return (
        response.status_code,
        _resp["m2m:grp"]["lt"],
    )  ## To get latest (entered data) instance


###########################################################################################################


@app.route("/delete", methods=["DELETE"])
def delete():
    request_json = request.get_json()  # Get JSON data from request
    device_name = request_json.get("device_name")
    device_type = request_json.get("device_type")
    device_group = request_json.get("device_group")
    uri = request.args.get("uri")  # Retrieve 'uri' from query parameters
    data_format = request.args.get(
        "data_format", "json"
    )  # Retrieve 'data_format' from query parameters, default is 'json'

    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{}".format(data_format),
    }

    response = requests.delete(uri, headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))

    # delete from db also
    if response.status_code == 200:
        delete_sensor_entry(
            sensor_name=device_name, sensor_type=device_type, group_name=device_group
        )
        delete_sensor_data(group_name=device_group, sensor_name=device_name)

    return "Success" if response.status_code == 200 else "Error"


###########################################################################################################


def discovery(uri="", data_format="json"):
    """
    Method description:
    Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
    under the specified CSE

    Parameters:
    uri_cse : [str] URI of parent CSE
    ae_name : [str] name of the AE
    fmt_ex : [str] payload format
    """
    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{}".format(data_format),
    }

    response = requests.delete(uri, headers=headers)
    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    _resp = json.loads(response.text)
    return response.status_code, _resp["m2m:uril"]


# ====================================================


@app.route("/createdevice", methods=["POST"])
def create_device():
    request_json = request.get_json()  # Get JSON data from request

    uri_ae = request_json.get("uri_ae")  # Retrieve uri_cse from JSON body
    device_name = request_json.get("device_name")
    device_type = request_json.get("device_type")
    device_group = request_json.get("device_group")
    device_description = request_json.get("device_description")
    device_labels = request_json.get("device_labels", "")
    description = request_json.get("description", "")
    data_format = request_json.get("data_format", "json")

    # checking whether the sensor name is previously not used
    if not is_name_available(device_name):
        print("*************************************************")
        return "Error"

    st1 = create_CNT(uri_ae, device_name, device_labels, data_format)
    st2 = create_CNT(
        uri_ae + device_name, device_name + "_descriptor", device_labels, data_format
    )
    st3 = create_desc_CIN(
        uri_ae + device_name + "/" + device_name + "_descriptor",
        description,
        device_labels,
        data_format,
    )
    st4 = create_CNT(uri_ae + device_name, device_name + "_data", ["data"], data_format)
    if st1 and st2 and st3 and st4:
        # db save
        register_sensor(
            group_name=device_group,
            sensor_type=device_type,
            sensor_name=device_name,
            description=device_description,
            data_info=description,
        )
        return "Success"
    return "Error"


def create_AE(uri_cse, ae_name, ae_labels, data_format):
    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{};ty=2".format(data_format),
    }

    body = {
        "m2m:ae": {
            "rn": "{}".format(ae_name),
            "api": "acp_admin",
            "rr": "true",  # resource reachable from CSE
            "lbl": ae_labels,
        }
    }

    try:
        response = requests.post(uri_cse, json=body, headers=headers)
    except TypeError:
        response = requests.post(uri_cse, data=json.dumps(body), headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    return True if response.status_code == 201 else False


def create_CNT(uri_ae, cnt_name, cnt_labels, data_format):
    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{};ty=3".format(data_format),
    }

    body = {"m2m:cnt": {"rn": "{}".format(cnt_name), "mni": 120, "lbl": cnt_labels}}

    try:
        response = requests.post(uri_ae, json=body, headers=headers)
    except TypeError:
        response = requests.post(uri_ae, data=json.dumps(body), headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    return True if response.status_code == 201 else False


def create_desc_CIN(uri_desc_cnt, node_description, desc_cin_labels, data_format):
    headers = {
        "X-M2M-Origin": "admin:admin",
        "Content-type": "application/{};ty=4".format(data_format),
    }

    body = {
        "m2m:cin": {
            "cnf": "application/json",
            "con": node_description,
            "lbl": desc_cin_labels,
        }
    }

    try:
        response = requests.post(uri_desc_cnt, json=body, headers=headers)
    except TypeError:
        response = requests.post(uri_desc_cnt, data=json.dumps(body), headers=headers)

    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))
    return True if response.status_code == 201 else False


processes = {}


@app.route("/rundevicescript", methods=["POST"])
def run_device_script():
    global processes
    process = None
    try:
        device_name = request.json.get("device_name")
        device_type = request.json.get("device_type")
        device_group = request.json.get("device_group")
        container = request.json.get("container")
        if not device_name or not container:
            return jsonify(
                {
                    "status": "error",
                    "message": "AE and container are required in the request body",
                }
            )
        if process and process.poll() is None:
            return jsonify({"status": "error", "message": "Script is already running"})
        # if device_type in ["Lamp", "Buzzer"]:
        #     # update in db
        #     toggle_sensor(
        #         group_name=device_group,
        #         sensor_name=device_name,
        #         sensor_type=device_type,
        #     )
        #     return jsonify(
        #         {
        #             "status": "success",
        #             "message": "Device type is servo, no continuous publishing of data required",
        #         }
        #     )

        process = Popen(
            [
                "python3",
                "mockdevice.py",
                device_name,
                device_group,
                device_type,
                container,
            ],
            stdout=PIPE,
            stderr=STDOUT,
        )
        output, _ = process.communicate()
        print(output.decode())
        processes[device_name] = process
        # update in db
        toggle_sensor(
            group_name=device_group, sensor_name=device_name, sensor_type=device_type
        )
        return jsonify(
            {
                "status": "success",
                "message": "Mock device script executed successfully -> "
                + device_name
                + " | "
                + device_group
                + " | "
                + device_type
                + " | "
                + container,
            }
        )
    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": "Failed to execute mock device script",
                "error": str(e),
            }
        )


@app.route("/stopdevicescript", methods=["POST"])
def stop_device_script():
    global processes
    device_name = request.json.get("device_name")  # Get "ae" value from request body
    device_type = request.json.get("device_type")
    device_group = request.json.get("device_group")
    process = processes.get(
        device_name
    )  # Get process associated with "ae" value from global dictionary
    try:
        # if device_type in ["Lamp", "Buzzer"]:
        #     # update in db
        #     toggle_sensor(
        #         group_name=device_group,
        #         sensor_name=device_name,
        #         sensor_type=device_type,
        #     )
        #     return jsonify(
        #         {
        #             "status": "success",
        #             "message": "Device type is servo, no continuous publishing of data required",
        #         }
        #     )
        if process and process.poll() is None:
            process.terminate()
            process = None
            # update in db
            toggle_sensor(
                group_name=device_group,
                sensor_name=device_name,
                sensor_type=device_type,
            )
            return jsonify(
                {"status": "success", "message": "Mock device script stopped"}
            )
        else:
            return jsonify({"status": "error", "message": "Script is not running"})
    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": "Failed to stop mock device script",
                "error": str(e),
            }
        )


# ------------------------ for sensor manager frontend ----------------------- #
@app.route("/getdevices", methods=["GET"])
def fetch_devices():
    return jsonify(fetch_sensors())


if __name__ == "__main__":
    app.run(port=8069, host="0.0.0.0")
