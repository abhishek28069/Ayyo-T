import os
import logging
import requests
import sqlite3 as _dbsql
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

from db import sync_sensor_data

onem2m_base_url = "http://onem2m_server:5089"

_db_root = "Database"
_dir = Path().resolve()

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)
iohandler = logging.StreamHandler()
iohandler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
iohandler.setFormatter(formatter)
_log.addHandler(iohandler)
logging.basicConfig(filename="execution_log.log", filemode="w")

try:
    os.chdir(_dir)
    _db_root_check = os.path.isdir(_db_root)
    if not _db_root_check:
        os.makedirs(_db_root)
    _db_path = os.path.join(_dir, _db_root)
    os.chdir(_db_path)
    _log.info("database root initialised successfully")
except Exception as _initialization_exception:
    _log.critical("root path could not be initialised")

try:
    _db_con = _dbsql.connect("inm_warehouse.db")
    _log.info("database inm_warehouse.db initialised successfully")
except Exception as _db_initialization:
    _log.critical("database could not be initialised")

try:
    _db_cursor = _db_con.cursor()
    _db_cursor.execute(
        """CREATE TABLE warehouse
               (device_name text not null, timestamp text not null, data text not null)"""
    )
    _log.info("database table creation successful")
except Exception as _db_exception:
    _log.warning("database table could not be initialised: " + str(_db_exception))


def get_descriptor(Node_name):
    url = (
        onem2m_base_url
        + "/~/in-cse/in-name/IIITH/"
        + Node_name
        + "/"
        + Node_name
        + "_descriptor/la"
    )

    payload = {}
    headers = {"X-M2M-Origin": "admin:admin", "Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        _log.warning("device not found")
        return False, None
    _data = eval(response.text)
    _con = _data["m2m:cin"]["con"].replace(" ", "")
    _con = _con.split("[")[1]
    _con = _con.split("]")[0]
    _con = _con.split(",")
    _log.info("data retrieved from om2m")
    print(_con)
    return True, _con


def get_from_db(_node_name):
    name = "'" + _node_name + "'"
    _data = _db_cursor.execute("SELECT * FROM warehouse where device_name =" + name)
    _log.info("data retrieved from db")
    return _data


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "/ngsi-ld/v1/entities/" in self.path:
            _node_name = self.path.split("/ngsi-ld/v1/entities/")[1]
            _parameter_list = ["node_id"]
            _om2m_status = get_descriptor(_node_name)
            print("name: ", _node_name)

            if not _om2m_status[0]:
                self.send_response(404)
                response = '{"type":"urn:dx:rs:general","title":"Device Not Registered","detail":"Device Not Registered"}'

            else:
                _lis = []
                self.send_response(200)
                _parameter_list += _om2m_status[1]
                _log.info(_parameter_list)
                response = '{"title": "Successful operation", "type": "urn:dx:rs:success", "results": ['

                _data = get_from_db(_node_name)
                for row in _data:
                    _log.info(row)
                    _lis += [row]
                _ordered_data = list(reversed(_lis))
                length_of_data = len(_ordered_data)
                for row_id in range(length_of_data):
                    _current_row = [_node_name]
                    _current_row += eval(list(_ordered_data[row_id])[2])
                    response += "{"
                    _data_length = len(_parameter_list)

                    for parameter_id in range(_data_length):
                        response += (
                            '"'
                            + _parameter_list[parameter_id]
                            + '":'
                            + '"'
                            + str(_current_row[parameter_id])
                        )

                        if parameter_id == _data_length - 1:
                            response += '"'

                        else:
                            response += '",'

                    if row_id == length_of_data - 1:
                        response += "}"

                    else:
                        response += "},"

                response += "]}"
                _log.info("data formatting successsful")

        else:
            _log.warning("url-end point not found")
            self.send_response(404)
            response = (
                '{"type":"urn:dx:rs:general","title":"NotFound","detail":"NotFound"}'
            )

        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(response, "utf8"))

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers["Content-Length"])).decode(
            "utf-8"
        )
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        try:
            print(self.data_string)
            var = self.data_string.replace("false", "False")
            var = eval(var.replace("true", "True"))
            _con = eval(var["m2m:sgn"]["m2m:nev"]["m2m:rep"]["m2m:cin"]["con"])
            _lbl = var["m2m:sgn"]["m2m:nev"]["m2m:rep"]["m2m:cin"]["lbl"]
            _values = (str(_lbl[0]), str(_con[0]), str(_con))
            sync_sensor_data(
                group_name=_lbl[0], sensor_name=_lbl[2], sensor_type=_lbl[1], data=_con
            )
            _log.info("data stored into supabase!")
        except Exception as ioerror:
            _log.critical("data storage failed with exception: " + str(ioerror))

        message = '{"Status": 200}'
        self.wfile.write(bytes(message, "utf8"))


with HTTPServer(("0.0.0.0", 5091), handler) as server:
    server.serve_forever()
