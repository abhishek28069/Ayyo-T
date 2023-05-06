import json 
import docker
import time
from flask import Flask, request
import zipfile
import os 
import logging
from config import app, db, module_config, bucket
from kafka import KafkaProducer
import threading
import socket



@app.route('/')
def index():
    return 'Deployer is running on ' + module_config['host_name'] + '@' + module_config['host_ip']

def extractAppZip(src_path, dest_path, instance_id):
    """
    Extracts a zip file from `src_path` to `dest_path`.
    """
    logging.info("Extracting zip file %s to %s", src_path, dest_path)
    with zipfile.ZipFile(src_path, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    extracted_folder_name = os.path.splitext(os.path.basename(src_path))[0]
    extracted_folder_path = os.path.join(dest_path, extracted_folder_name)
    new_folder_path = os.path.join(dest_path, instance_id)
    logging.info("Renaming extracted folder %s to %s", extracted_folder_path, new_folder_path)
    try:
        os.rename(extracted_folder_path, new_folder_path)
        os.remove(f"/tmp/app.zip")
        logging.info("Deleted app.zip")

    except Exception as e:
        logging.error("Error while renaming extracted folder or deleting app.zip: %s", e)


def docker_host_ip():
    # Create a socket to connect to Google DNS and get the IP address of the default route
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        docker_host_ip = s.getsockname()[0]
    return docker_host_ip

def find_free_port():
    # create a temporary socket to find a free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # bind to any available port
        port = s.getsockname()[1]  # get the assigned port
    return port

def find_free_port_on_host():
    # Get the IP address of the Docker host
    docker_host = docker_host_ip()
    # Create a socket and bind it to a random port on the Docker host
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((docker_host, 0))
        port = s.getsockname()[1]
    return port


def deploy_app_thread(application_id, instance_id, sensor_bindings):
    # application = db.apps.find_one({"ApplicationID": application_id})
    # # Get the file ID from the document
    # file_id = application["content"]
    # Get the file from MongoDB using GridFS
    try:
        db.update({"status": "pending"}).eq("instance_id", instance_id).execute()
    except:
        logging.info("Row update failed")

    files = bucket.list(application_id)
    # Save the file to disk
    # with open(f"/tmp/{application_id}.zip", "wb") as f:
    #     f.write(file_data)

    for file in files:
        file_name = file['name']
        file_path = f"{application_id}/{file_name}"
        destination_path = f"/tmp/{file_name}"
        
        try:
            with open(destination_path, 'wb+') as f:
                res = bucket.download(file_path)
                logging.info(f"Downloaded {file_name} to {destination_path}")
                print(f"Downloaded {file_name} to {destination_path}")
                if file_name.endswith('.json'):
                    app_contract = json.loads(res)
                else:
                    f.write(res)
        except:
            logging.warning(f"Failed to download {file_name}")

    extractAppZip(f"/tmp/app.zip", "/tmp/", instance_id)
    # os.remove(f"/tmp/{instance_id}.zip")

    # app_contract = application['app_contract']

    #get a free port
    port = find_free_port()

    #Generate dockerfile for
    genDockerFile(port, instance_id)
    
    logging.info(type(sensor_bindings))
    #create sensor binding file 
    binding_file_path = f"/tmp/{instance_id}/src/bindings.json"
    with open(binding_file_path, "w") as outfile:
        # Use the json.dumps() method to convert sensor_bindings to a JSON string with double quotes
        json_string = json.dumps(sensor_bindings)
        # Write the JSON string to the file
        outfile.write(json_string)
    
    deploy_instance(app_contract['app_name'], port, instance_id, f"/tmp/{instance_id}")
    logging.info("Application ID: %s deployed successfully for instance ID: %s", application_id, instance_id)

def stop_instance_thread(container_id, instance_id):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
        logging.info('Stopping container: ' + container_id)
        container.stop()
        logging.info('Stopped container: ' + container_id)
        logging.info('Removing container: ' + container_id)
        container.remove()
        logging.info('Removed container: ' + container_id)
    except Exception:
        logging.info('Container not found')
    
    try:
        db.update({"status": "stopped"}).eq("instance_id", instance_id).execute()
    except:
        logging.info("Row update failed")
        
    logging.info('Removed instance from db')

def genDockerFile(port, instance_id):
    logging.info("Generating Dockerfile for instance %s", instance_id)
    dockerfile = 'FROM node:18-alpine\n'
    dockerfile += 'WORKDIR /app\n'
    dockerfile += f'COPY package.json ./\n'
    dockerfile += 'RUN npm install\n'
    dockerfile += 'COPY . .\n'
    dockerfile += 'EXPOSE ' + str(port) + '\n'
    dockerfile += 'CMD ["npm", "run", "start"]'
    # create dockerfile
    with open(f'/tmp/{instance_id}/Dockerfile', 'w') as f:
        f.write(dockerfile)
    logging.info("Dockerfile generated successfully for instance %s", instance_id)

def deploy_instance(image_name, port,  instance_id, dockerfile_dir=".",):
    # Create a Docker client object that connects to the Docker daemon on the host machine
    docker_client = docker.from_env()
    # Build the Docker image
    logging.info(f"Building Docker image: {image_name}")
    docker_client.images.build(path=dockerfile_dir, tag=image_name)

    # get free host port
    host_port = find_free_port_on_host()
    # Run the image
    container = docker_client.containers.run(
        image=image_name,
        detach=True,
        ports={f"{port}/tcp": host_port},
        environment={
            "PORT_NUMBER": str(port)
        })
    
    # Update the db with container id
    container = docker_client.containers.get(container.id)
    try:
        db.update({"container_id": container.id, "status": "complete", "port": host_port}).eq("instance_id", instance_id).execute()
    except:
        logging.warning("Failed to update database row")
    logging.info('Container: ' + container.id +
                 ' status: ' + container.status)



@app.route('/app', methods=['POST'])
def deploy_app():
    app_id = request.json['ApplicationID']
    instance_id = request.json['InstanceID']
    sensor_bindings = request.json['SensorBindings']
    # TODO: validate the application ID from the database
    res = db.select("*").eq("app_id", app_id).execute()
    if res.data and len(res.data) >0:
        # Return an error response if the ID is not found
        
        logging.info('Received valid application ID: %s for instance ID: %s', app_id, instance_id)
        threading.Thread(target=deploy_app_thread, args=(app_id, instance_id, sensor_bindings)).start()
        logging.info('Successfully deployed application ID: %s for instance ID: %s', app_id, instance_id)

        return {"InstanceID": instance_id,"app_id":app_id, "Status": "pending"}

    logging.warning('Received invalid application ID: %s for instance ID: %s', app_id, instance_id)
    return {"error": "Invalid application ID"}
    


@app.route('/stop-instance', methods=['POST'])
def stop_instance():
    print("recieved stop request at slave")
    instance_id = request.json['InstanceID']
    container_id = request.json['ContainerID']
    threading.Thread(target=stop_instance_thread, kwargs={
                     'instance_id': instance_id, 'container_id': container_id}).start()
    return {"InstanceID": instance_id, "Status": "stopping"}

def run_monitoring_thread():
    def json_serializer(data):
        return json.dumps(data).encode("utf-8")
    producer=KafkaProducer(bootstrap_servers=['20.75.91.206:9092'],api_version=(0, 10, 1),
                        value_serializer=json_serializer)
    while True:
        producer.send("deployer_to_monitoring","scheduler is alive")
        time.sleep(20)

if __name__ == '__main__':
    monitoring_thread = threading.Thread(target=run_monitoring_thread)
    monitoring_thread.start()
    app.run(host='0.0.0.0', port=8081)