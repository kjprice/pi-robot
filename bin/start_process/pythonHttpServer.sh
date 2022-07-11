#!/bin/bash

cd "$(dirname "$0")"

../misc/setup_shell.sh

python_port=`../misc/get_config.sh portsByProcess.pythonHttpServer`
../misc/kill_process_on_port.sh $python_port

python -m http.server $python_port