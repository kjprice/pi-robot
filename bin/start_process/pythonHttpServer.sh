#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh

python_port=`../misc/get_config.sh portsByProcess.pythonHttpServer`
../misc/kill_process_on_port.sh $python_port

cd ../../
python -m python.pi_applications.run_simple_server $other_args
