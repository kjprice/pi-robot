#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh
python_port=`../misc/get_config.sh ports.pythonHttpServer`

log_dir=`../misc/get_config.sh logDirectoriesByProcess.pythonHttpServer`
../misc/kill_process_on_port.sh $python_port
echo "Listening on port $python_port"

# Surpress output
pushd () {
    command pushd "$@" > /dev/null
}
popd () {
    command popd "$@" > /dev/null
}

pushd ../../data/
log_filename=$(date '+%Y-%m-%d_%H_%M_%S').txt
log_dir=logs/$log_dir
mkdir -p $log_dir
log_path=$log_dir/$log_filename

python -m http.server $python_port >> $log_path 2>&1 &
popd

process_id="$!"

cd ../..
process_name=pythonHttpServer
echo "Setting new process '$process_name' with process id '$process_id'"
python -m python.modules.processes.process_id set $process_name $process_id