# Use an official Python runtime as a parent image
FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk

# Set the working directory to /onem2m_server
WORKDIR /app

# Copy the contents of the local app directory to the container at /app
COPY app /app

# Give execute permission to the start.sh script
RUN chmod +x start.sh

EXPOSE 5089

# Set the user to root
USER root

# Run the start.sh script
CMD ["bash", "-c", "./start.sh"]

