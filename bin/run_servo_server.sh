#!/bin/sh
cd "$(dirname "$0")"

export PORT=5000

filename=$(basename "$0")
./kill_process_by_name.sh $filename
./kill_process_on_port.sh $PORT

cd ../python

export FLASK_APP=run_servo_server.py
# lsof -ti tcp:5000 | xargs kill
flask run --host=0.0.0.0 --port $PORT