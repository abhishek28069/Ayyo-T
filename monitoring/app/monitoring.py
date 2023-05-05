import logging
from kafka import KafkaConsumer, errors
from kafka import KafkaProducer
import json
import threading
import time

kafka_url = "20.75.91.206:9092"

# Set up logger
logging.basicConfig(filename='monitoring.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer=KafkaProducer(bootstrap_servers=[kafka_url],api_version=(0, 10, 1),
                       value_serializer=json_serializer)


def send_restart_msg(msg):
    try:
        future =  producer.send('monitoring_to_platform_initializer', msg)
        print('Message sent successfully')
    except errors.KafkaError as e:
        print('Failed to send message:', e)
    finally:
        time.sleep(20)

def monitoring_deployer():
    consumer=KafkaConsumer("deployer_to_monitoring",bootstrap_servers=kafka_url,
                           auto_offset_reset='latest',group_id='consumer-group-a',
                           consumer_timeout_ms = 80000)
    def recurr():
        for msg in consumer:
            logging.info("message received from deployer")
        msg = {"module": "deployer"}
        send_restart_msg(msg)
        recurr()
    recurr()
    
def monitoring_deployer_master():
    consumer=KafkaConsumer("deployer_master_to_monitoring",bootstrap_servers=kafka_url,
                           auto_offset_reset='latest',group_id='consumer-group-b',
                           consumer_timeout_ms = 80000)
    def recurr():
        for msg in consumer:
            logging.info("message received from deployer master")
        msg = {"module": "deployer_master"}
        send_restart_msg(msg)
        recurr()
    recurr()

def monitoring_scheduler():
    consumer=KafkaConsumer("scheduler_to_monitoring",bootstrap_servers=kafka_url,
                           auto_offset_reset='latest',group_id='consumer-group-c',
                           consumer_timeout_ms = 80000)
    def recurr():
        for msg in consumer:
            logging.info("message received from scheduler")
        msg = {"module": "scheduler"}
        send_restart_msg(msg)
        recurr()
    recurr()
    

def monitoring_sensor_manager():
    consumer=KafkaConsumer("sensor_manager_to_monitoring",bootstrap_servers=kafka_url,
                           auto_offset_reset='latest',group_id='consumer-group-d',
                           consumer_timeout_ms = 80000)
    def recurr():
        for msg in consumer:
            logging.info("message received from sensor_manager")
        msg = {"module": "sensor_manager"}
        send_restart_msg(msg)
        recurr()
    recurr()

def monitoring_platform_backend():
    consumer=KafkaConsumer("platform_backend_to_monitoring",bootstrap_servers=kafka_url,
                           auto_offset_reset='latest',group_id='consumer-group-e',
                           consumer_timeout_ms = 80000)
    def recurr():
        for msg in consumer:
            logging.info("message received from platform_backend")
        msg = {"module": "platform_backend"}
        send_restart_msg(msg)
        recurr()
    recurr()



    

if __name__=='__main__':
    logging.info("[*] SCHEDULER ON")
    # Create threads
    monitoring_scheduler_thread = threading.Thread(target=monitoring_scheduler)
    monitoring_deployer_master_thread = threading.Thread(target=monitoring_deployer_master)
    monitoring_deployer_thread = threading.Thread(target=monitoring_deployer)
    monitoring_sensor_manager_thread = threading.Thread(target=monitoring_sensor_manager)
    monitoring_platform_backend_thread = threading.Thread(target=monitoring_platform_backend)
    # Start threads
    monitoring_scheduler_thread.start()
    monitoring_deployer_master_thread.start()
    monitoring_deployer_thread.start()
    monitoring_sensor_manager_thread.start()
    monitoring_platform_backend_thread.start()



    