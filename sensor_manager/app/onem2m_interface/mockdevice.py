import os
import time
import math
import json
import random
import threading
import requests
import sys

from faker import *

data_frequency = 3  # 3 seconds

onem2m_base_url = "http://onem2m_server:5089"
onem2m_warehouse_base_url = "http://sensor_manager:5091/"


def get_rand_data(device_type):
    # Call the appropriate function based on the device type
    if device_type == "Temperature":
        return generate_fake_temperature()
    elif device_type == "Humidity":
        return generate_fake_humidity()
    elif device_type == "Luminosity":
        return generate_fake_luminosity()
    elif device_type == "Power":
        return generate_fake_electricity_consumption()
    elif device_type == "Solar":
        return generate_fake_solar_energy()
    elif device_type == "Air Quality":
        return generate_fake_air_quality()
    elif device_type == "Presence":
        return generate_fake_presence()
    elif device_type == "Lamp":
        return generate_fake_lamp_clicks()
    elif device_type == "Buzzer":
        return generate_fake_buzzer()
    else:
        raise ValueError("Invalid device type")


def post_random_data(device_name, device_group, device_type, container):
    timestamp = int(time.time())

    generated_data = get_rand_data(device_type)

    _data_cin = [timestamp, generated_data]

    url = onem2m_base_url + "/~/in-cse/in-name/IIITH/{}/{}".format(
        device_name, container
    )

    headers = {"X-M2M-Origin": "admin:admin", "Content-Type": "application/json;ty=4"}

    payload = {
        "m2m:cin": {
            "con": str(_data_cin),
            "lbl": [device_group, device_type, device_name, container],
            "cnf": "text",
        }
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.text)
    return response.status_code


def run(device_name, device_group, device_type, container):
    publish_count = 0
    while True:
        # status_code = post_random_multi_data()
        status_code = post_random_data(
            device_name, device_group, device_type, container
        )
        if status_code == 201:
            publish_count += 1
            print("Data publishing at " + str(data_frequency) + "-second frequency")
            print("Publish Successful")
            print("Number of data point published = " + str(publish_count))
        else:
            print(
                "Unable to publish data, process failed with a status code: "
                + str(status_code)
            )
        time.sleep(data_frequency)


def subscribe(device_name):
    url = (
        onem2m_base_url
        + "/~/in-cse/in-name/IIITH/"
        + device_name
        + "/"
        + device_name
        + "_data"
    )
    headers = {"X-M2M-Origin": "admin:admin", "Content-Type": "application/json;ty=23"}
    payload = {"m2m:sub": {"rn": "Sub-DW", "nct": 2, "nu": onem2m_warehouse_base_url}}

    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.text)
    response.text


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 mockdevice.py <ae> <container>")
    else:
        device_name = sys.argv[1]
        device_group = sys.argv[2]
        device_type = sys.argv[3]
        container = sys.argv[4]
        subscribe(device_name)
        run(device_name, device_group, device_type, container)


def run_mock_device(device_name, device_group, device_type, container):
    subscribe(device_name)
    run(device_name, device_group, device_type, container)
