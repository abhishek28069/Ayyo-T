import os
import json
from supabase import create_client

url = "https://zakntpuxbdegdkyvdzkw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpha250cHV4YmRlZ2RreXZkemt3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODEyODIyNjEsImV4cCI6MTk5Njg1ODI2MX0.qJp48cSwfb0QKFOE-TAB22yJN_m6rU6kK5Ers_GgcHM"
supabase = create_client(url, key)


# ------------ util to insert row in db given table name and data ------------ #
def insert_into(table_name, value):
    # value is a dictionary
    data, count = supabase.table(table_name).insert(value).execute()


# --------------------------- create a sensor entry -------------------------- #
def register_sensor(group_name, sensor_type, sensor_name, description, data_info):
    value = {
        "group_name": group_name,
        "sensor_type": sensor_type,
        "sensor_name": sensor_name,
        "description": description,
        "data_info": data_info,
    }
    insert_into("sensor_registry", value)


# -------------------------- get all sensor entries -------------------------- #
def fetch_sensors():
    data, _ = supabase.table("sensor_registry").select("*").order("created_at", desc=True).execute()
    print(data)
    return data[1]


# ------------------- check if the sensor name is available ------------------ #
def is_name_available(sensor_name):
    data, _ = (
        supabase.table("sensor_registry")
        .select("sensor_name")
        .eq("sensor_name", sensor_name)
        .execute()
    )
    if len(data[1]) == 0:
        return True
    else:
        return False


# --------------------- delete sensor entry and its data --------------------- #
def delete_sensor_entry(group_name, sensor_type, sensor_name):
    supabase.table("sensor_registry").delete().eq("group_name", group_name).eq(
        "sensor_type", sensor_type
    ).eq("sensor_name", sensor_name).execute()


def delete_sensor_data(group_name, sensor_name):
    supabase.table("sensor_data").delete().eq("group_name", group_name).eq(
        "sensor_name", sensor_name
    ).execute()


# delete_sensor_entry(group_name="H-105", sensor_type="Temperature", sensor_name="t1")
# delete_sensor_data(group_name="H-105", sensor_name="t1")


# ------------------------- toggle sensor activation ------------------------- #
def toggle_sensor(group_name, sensor_type, sensor_name):
    data, _ = (
        supabase.table("sensor_registry")
        .select("activated")
        .eq("group_name", group_name)
        .eq("sensor_type", sensor_type)
        .eq("sensor_name", sensor_name)
        .execute()
    )
    activated = "FALSE" if data[1][0]["activated"] else "TRUE"
    supabase.table("sensor_registry").update({"activated": activated}).eq(
        "group_name", group_name
    ).eq("sensor_type", sensor_type).eq("sensor_name", sensor_name).execute()


# toggle_sensor("H-105", "Temperature", "t1")


# ------------------------- publish onem2m data to db ------------------------ #
def sync_sensor_data(group_name, sensor_name, sensor_type, data):
    value = {
        "group_name": group_name,
        "sensor_name": sensor_name,
        "sensor_type": sensor_type,
        "data": data,
    }
    insert_into("sensor_data", value)


# --------------------------- create sensor binding -------------------------- #
# value = {"app_id": 2, "binded_sensors": ["1", "2"]}
# insert_into("sensor_binding", value)


# ------------------------- to modify binded sensors ------------------------- #
def update_binded_sensors(app_id, value):
    data, count = (
        supabase.table("sensor_binding").update(value).eq("app_id", app_id).execute()
    )


# value = {"app_id": 2, "binded_sensors": ["new1", "new2"]}
# update_binded_sensors(value=value, app_id=1)


# --------------------------- fetch binded sensors --------------------------- #
# data, count = supabase.table("sensor_binding").select("*").eq("app_id", 2).execute()
# print(data[1][0]["binded_sensors"])
