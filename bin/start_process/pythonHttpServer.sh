#!/bin/bash

cd "$(dirname "$0")"

log_path=$1

../misc/setup_shell.sh

python_port=`../misc/get_config.sh portsByProcess.pythonHttpServer`
../misc/kill_process_on_port.sh $python_port

cd ../../data

python -m http.server $python_port >> ../$log_path 2>&1 &

process_id="$!"
echo $process_id
