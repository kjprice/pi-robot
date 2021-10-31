#!/bin/bash
cd "$(dirname "$0")"
cd ../python

source ~/.bash_profile
ca

# script_to_run=run_camera_head_server.py
# script_to_run=modules/process_image_for_servo.py
script_to_run=modules/servo_module.py
# script_to_run=run_servo_server.py


nodemon -e py,sh -x "time IS_TEST=true python3.6 $script_to_run"
