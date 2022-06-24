#!/bin/bash
cd "$(dirname "$0")"
../misc/setup_shell.sh

script_to_run=run_camera_head_server.sh
# script_to_run=modules/process_image_for_servo.py
# script_to_run=modules/servo_module.py
# script_to_run=run_servo_server.py

cd ../..
nodemon -e py,sh -x "IS_TEST=true ./bin/run/$script_to_run || true"