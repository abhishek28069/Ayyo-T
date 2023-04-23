from kafka import KafkaConsumer
import json


consumer1 = KafkaConsumer(
	'app_zips',
    max_partition_fetch_bytes=20971520,
    fetch_max_bytes=20971520,
)

for msg in consumer1:
    blob_data = msg.value
    with open('./files/app.zip', 'wb') as f:
        f.write(msg.value)
        print('File saved')



consumer2 = KafkaConsumer(
	'scheduled_apps',
    max_partition_fetch_bytes=20971520,
	fetch_max_bytes=20971520,
	value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
for msg in consumer2:
	print(msg.value)
