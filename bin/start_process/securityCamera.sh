#!/bin/bash

cd "$(dirname "$0")"

log_path=$1

source ../misc/setup_shell.sh

# Kill services that might use the camera
../misc/kill_process_by_name.sh robotCameraHead >> ../../$log_path 2>&1

../run/run_security_camera_forever.sh >> ../../$log_path 2>&1 &

process_id="$!"

echo $process_id