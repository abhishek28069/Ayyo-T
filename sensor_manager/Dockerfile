# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the local app directory to the container at /app
COPY app /app

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Expose ports
EXPOSE 8069
EXPOSE 5091
EXPOSE 2000

# Start the servers in separate terminals
CMD ["bash", "-c", "python3 /app/onem2m_interface/onem2mapi.py & python3 /app/onem2m_interface/onem2mDataWarehouse.py & python3 /app/sensor_query/query_server.py"]

