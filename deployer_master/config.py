from flask import Flask
from kafka_helper import KafkaAdmin
from supabase import create_client
import json
import importlib.resources as pkg_resources


app = Flask(__name__)
with open('config.json') as f:
    module_config = json.load(f)

kafka_server = "{}:{}".format(module_config['kafka_ip'], module_config['kafka_port'])
# messenger = KafkaAdmin(kafka_server, 'platform_manager')
client = create_client(module_config['supabase_url'], module_config['supabase_key'])
db = client.table("app_instance_states")
