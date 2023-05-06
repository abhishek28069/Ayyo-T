import schedule
import time
import threading 
#Kafka to be configured on local machine and then run
from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import logging
# logging.config(bas)
#cron job format (day to be added later)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')
def json_serializer(data):
    return json.dumps(data).encode("utf-8")
consumer=KafkaConsumer("scheduled_apps3",bootstrap_servers=' 20.75.91.206:9092',auto_offset_reset='latest',group_id='consumer-group-a')

producer=KafkaProducer(bootstrap_servers=['20.75.91.206:9092'],api_version=(0, 10, 1),
                       value_serializer=json_serializer)
def cron(app_id,instance_id,start_time,end_time,sensor_bindings,day):
    # logging.info(day+ start_time+ end_time)
    if day == "monday":
        schedule.every().monday.at(start_time).do(deployer_message, app_id,instance_id,sensor_bindings,0)
        schedule.every().monday.at(end_time).do(deployer_message, app_id,instance_id,sensor_bindings,1)
    if day == "tuesday":
        schedule.every().tuesday.at(start_time).do(deployer_message, app_id,instance_id,sensor_bindings,0)
        schedule.every().tuesday.at(end_time).do(deployer_message, app_id,instance_id,sensor_bindings,1)
    if day == "wednesday":
        schedule.every().wednesday.at(start_time).do(deployer_message, app_id,instance_id,sensor_bindings,0)
        schedule.every().wednesday.at(end_time).do(deployer_message, app_id,instance_id,sensor_bindings,1)
    if day == "thursday":
        schedule.every().thursday.at(start_time).do(deployer_message, app_id,instance_id,sensor_bindings,0)
        schedule.every().thursday.at(end_time).do(deployer_message, app_id,instance_id,sensor_bindings,1)
    if day == "friday":
        schedule.every().friday.at(start_time).do(deployer_message, app_id,instance_id,sensor_bindings,0)
        schedule.every().friday.at(end_time).do(deployer_message, app_id,instance_id,sensor_bindings,1)
    if day == "saturday":
        schedule.every().saturday.at(start_time).do(deployer_message, app_id,instance_id,sensor_bindings,0)
        schedule.every().saturday.at(end_time).do(deployer_message, app_id,instance_id,sensor_bindings,1)
    if day == "sunday":
        schedule.every().sunday.at(start_time).do(deployer_message, app_id,instance_id,sensor_bindings,0)
        schedule.every().sunday.at(end_time).do(deployer_message, app_id,instance_id,sensor_bindings,1)

#app to be run by deployer. Communication medium to be made later
def deployer_message(app_id,app_name,instance_id,sensor_bindings,flag):
    # print("hello")
    logging.info("in deployer function")
    if flag == 0:
        logging.info(str(app_id) + " Start sent to deployer")
        #line to be activated when kafka is configured
        data={
            "app_id":app_id,
            "app_name":app_name,
            "instance_id":instance_id,
            "type":"start",
            "sensor_bindings":sensor_bindings

        }
        producer.send('scheduler_to_deployer3', data)
        # data[] = scheduling info & instance ID
    else:
        data={
            "app_id":app_id,
            "app_name":app_name,
            "instance_id":instance_id,
            "type":"stop",
            "sensor_bindings":sensor_bindings
        }
        logging.info(str(app_id) + " End sent to deployer")
        producer.send('scheduler_to_deployer3', data)

def decode_json(app_crons):
    logging.info("decoding_json")
    print(app_crons)
    logging.info(app_crons)
    app_id = app_crons["app_id"]
    app_name = app_crons["app_name"]
    instance_id=app_crons["instance_id"]
    user_kill=app_crons["user_kill"]
    if user_kill == 1:
        deployer_message(app_id,app_name,instance_id,"",1)
        return
    sched_info = app_crons["schedule_info"]["timings"]
    sched_flag = app_crons["sched_flag"]
    sensor_bindings=app_crons["sensor_bindings"]
    if sched_flag == 0:
        deployer_message(app_id,app_name,instance_id,sensor_bindings,0)
        return
    else:
        logging.info("hellooo")
        for day in sched_info:
            start_time = sched_info[day]["start_hour"]
            end_time = sched_info[day]["end_hour"]
            if start_time!="" and end_time!="":
                cron(app_id,instance_id,start_time,end_time,sensor_bindings,day)
                
def get_schedule_info_thread():
    logging.info("starting the consumer")
    # print("adsf")
    for msg in consumer:
        app_crons = json.loads(msg.value)
        logging.info(app_crons)
        decode_json(app_crons)

#data input format : app_id, schedule_datetimestamp_start, schedule_datetimestamp_start
def run_pending_jobs_thread():
    logging.info("inside run pending jobs")
    i=0
    while True:
        schedule.run_pending()
        # time.sleep(1)

def run_monitoring_thread():
    def json_serializer(data):
        return json.dumps(data).encode("utf-8")
    producer=KafkaProducer(bootstrap_servers=['20.75.91.206:9092'],api_version=(0, 10, 1),
                        value_serializer=json_serializer)
    while True:
        producer.send("scheduler_to_monitoring","scheduler is alive")
        time.sleep(20)

if __name__ == "__main__":
    logging.info("[*] SCHEDULER ON")
    # Create threads
    get_schedule_thread = threading.Thread(target=get_schedule_info_thread)
    run_pending_thread = threading.Thread(target=run_pending_jobs_thread)
    monitoring_thread = threading.Thread(target=run_monitoring_thread)
    # Start threads
    get_schedule_thread.start()
    run_pending_thread.start()
    monitoring_thread.start()

    # Join threads to wait for them to complete
    # get_schedule_thread.join()
    # run_pending_thread.join()

    # logging.info("All threads finished")
