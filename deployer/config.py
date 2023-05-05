from flask import Flask
from supabase import create_client
import json
import importlib.resources as pkg_resources
import logging


app = Flask(__name__)
with open('config.json') as f:
    module_config = json.load(f)


# kafka_server = "{}:{}".format(module_config['kafka_ip'], module_config['kafka_port'])
# mongo_server = "{}:{}".format(
#     module_config['mongo_ip'], module_config['mongo_port'])

# client = MongoClient(module_config['mongo_server'])

# db = client.sample_application
# fs = gridfs.GridFS(db)
client = create_client(module_config['supabase_url'], module_config['supabase_key'])
db = client.table("app_instance_states")
bucket = client.storage.from_("application")