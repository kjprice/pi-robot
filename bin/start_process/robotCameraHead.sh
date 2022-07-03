#!/bin/bash

cd "$(dirname "$0")"

log_path=$1
other_args=$2

source ../misc/setup_shell.sh

# Kill services that might use the camera
../misc/kill_process_by_name.sh securityCamera >> ../../$log_path 2>&1

# Download model to detect faces
../download/download_model.sh >> ../../$log_path 2>&1

cd ../../

python -m python.pi_applications.run_camera_head_server $other_args >> ./$log_path 2>&1 &

process_id="$!"
echo $process_id