#!/bin/bash

cd "$(dirname "$0")"

other_args=$1

source ../misc/setup_shell.sh

# Kill services that might use the camera
../misc/kill_process_by_name.sh securityCamera

# Download model to detect faces
../download/download_model.sh

cd ../../

python -m python.pi_applications.run_camera_head_server $other_args
