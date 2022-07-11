#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh

# Kill services that might use the camera
../misc/kill_process_by_name.sh robotCameraHead

../run/run_security_camera_forever.sh