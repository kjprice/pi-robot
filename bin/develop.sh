#!/bin/bash
cd "$(dirname "$0")"
cd ../python

source ~/.bash_profile
ca

# script_to_run=run-camera-head.py
script_to_run=modules/process_image_for_servo.py
# script_to_run=modules/servo_module.py

nodemon -e py,sh -x "time IS_TEST=true python $script_to_run"
