#!/bin/bash

# Save the current directory
APP_ROOT=$(pwd)

# Define a function to build and tag Docker image
build_and_tag() {
  local folder_name=$1
  cd "./$folder_name"
  docker build -t "$folder_name" .
  docker tag "$folder_name" "abhishek28069/unisense:$folder_name"
  docker push "abhishek28069/unisense:$folder_name"
  docker pull "abhishek28069/unisense:$folder_name"
  # Return to the app root directory
  cd "$APP_ROOT"
}

# Build and tag images in parallel
build_and_tag "onem2m_server" &
build_and_tag "platform_ui" &
build_and_tag "platform-backend" &
build_and_tag "sensor_manager" &
build_and_tag "sensormanager_frontend" &
build_and_tag "deployer" &
build_and_tag "deployer_master" &
build_and_tag "scheduler" &
build_and_tag "monitoring" &

# Wait for all parallel processes to finish
wait

