#!/bin/bash
cd "$(dirname "$0")"

# script_to_run=run_camera_head_server.sh
# script_to_run=run_processing_server.sh
# script_to_run=modules/process_image_for_servo.py
# script_to_run=modules/servo_module.py
# script_to_run=run_servo_server.sh
script_to_run=run_web_server.sh
# script_to_run=run_server_status_server.sh

cd ../..
nodemon -e py,sh,js -x "IS_TEST=true ./bin/run/$script_to_run || true"