import logging
from kafka import KafkaConsumer
import json
import os
import threading

kafka_url = "20.75.91.206:9092"

# Set up logger
logging.basicConfig(filename='platform_initializer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')


def platform_re_init():
    print("restarting entered")
    consumer=KafkaConsumer("monitoring_to_platform_initializer",bootstrap_servers=kafka_url,
                           auto_offset_reset='latest',group_id='consumer-group-a')
    
    for msg in consumer:
        print("restarting", msg.value)
        logging.info("message received from monitoring")
        logging.info(json.loads(msg.value))
        # run docker compose up
        platform_init()

def platform_init():
    os.system("cd ..")
    os.system('docker compose up')


if __name__ == "__main__":
    platform_init()
    threading.Thread(target=platform_re_init).start()