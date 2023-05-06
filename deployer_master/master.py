
import logging
from config import app, db, module_config, kafka_server
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
import requests
import time


# consumer = KafkaConsumer('scheduler_to_deployer', bootstrap_servers=kafka_server, enable_auto_commit=True)
consumer = KafkaConsumer('scheduler_to_deployer3', bootstrap_servers=kafka_server, enable_auto_commit=True)


@app.route('/')
def index():
    return 'Deployer master is running on ' + module_config['host_name'] + '@' + module_config['host_ip']

def deploy_app(message):
    application_id = message['app_id']
    app_name = message['app_name']
    instance_id = message['instance_id']
    sensor_bindings = message['sensor_bindings']

    try:
        db.insert({
                "instance_id": instance_id,
                "container_id": "",
                "app_name": app_name,
                "app_id": application_id,
                "status": "init",
                }).execute()
    except:
        logging.info("Row insertion failed")
    print("before sending...")
    print(f'{module_config["load_balancer"]}app')
    print({'ApplicationID': application_id, 'InstanceID': instance_id})
    res = requests.post(f'{module_config["load_balancer"]}app', json={
                        'ApplicationID': application_id, 'InstanceID':instance_id,
                        'SensorBindings':sensor_bindings})
    print("after sending...")
    logging.info("Sent request to app service")
    print(res.text)
    return res.text

def stop_instance(message):
    instance_id = message['instance_id']

    try:
        instance = db.select("*").eq('instance_id', instance_id).execute().data[0]

    except:
        logging.info("Couldn't find a row with the given instance id to be stoped")
        return {"InstanceID": instance_id, "Status": "not found"}

    # if instance['status'] != 'complete':
    #     return {"InstanceID": instance_id, "Status": "not running"}
    print("trying to send the stop reques to slave")
    res = requests.post(f'{module_config["load_balancer"]}stop-instance', json={
                        'InstanceID': instance_id, 'ContainerID': instance['container_id']})
    return res.text


def platform_req_thread():
    logging.info("Inside kafka thread")
    for message in consumer:
        message = json.loads(message.value.decode('utf-8'))
        if message['type'] =='start':
            logging.info("New app deploy request")
            print(message)
            threading.Thread(target=deploy_app, args=(message,)).start()
        elif message['type'] =='stop':
            print(message)
            logging.info("instance stop request recieved")
            logging.info(message)
            threading.Thread(target=stop_instance, args=(message,)).start()
            
def run_monitoring_thread():
    def json_serializer(data):
        return json.dumps(data).encode("utf-8")
    producer=KafkaProducer(bootstrap_servers=['20.75.91.206:9092'],api_version=(0, 10, 1),
                        value_serializer=json_serializer)
    while True:
        producer.send("deployer_master_to_monitoring","scheduler is alive")
        time.sleep(20)

if __name__ == '__main__':
    logging.info("Starting model deployment thread")    
    threading.Thread(target=platform_req_thread).start()
    threading.Thread(target=run_monitoring_thread).start()
    app.run(host='0.0.0.0', port=8080)