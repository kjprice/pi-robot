#!/bin/bash

cd "$(dirname "$0")"

other_args=$1

source ../misc/setup_shell.sh

# Kill services that might use the camera
../misc/kill_process_by_name.sh robotCameraHead

# ../run/run_security_camera_forever.sh

cd ../../

python -m python.pi_applications.run_security_camera $other_args
