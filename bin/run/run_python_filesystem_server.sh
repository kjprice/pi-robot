#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh
python_port=`../misc/get_config.sh pythonFileSystemServerPort`
log_dir=`../misc/get_config.sh logDirectoriesByProcess.pythonFileSystemDir`
../misc/kill_process_on_port.sh $python_port
echo "Listening on port $python_port"

cd ../../data/
python -m http.server $python_port >> $log_dir 2>&1 &
