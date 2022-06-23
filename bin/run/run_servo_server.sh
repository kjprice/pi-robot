#!/bin/sh
cd "$(dirname "$0")"
../misc/setup_shell.sh

export PORT=5000

../misc/kill_process_on_port.sh $PORT

cd ../..

# TODO: Modules are not going to work, should run through main: `python -m python.main``
# python python/pi_applications/run_camera_head_server.py
export FLASK_APP=python/pi_applications/run_camera_head_server.py
# lsof -ti tcp:5000 | xargs kill
flask run --host=0.0.0.0 --port $PORT
