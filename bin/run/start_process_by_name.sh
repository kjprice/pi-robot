#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh

process_name=$1

echo "Attempting to start new process with name '$process_name'"

../misc/kill_process_by_name.sh $process_name

log_path=`../misc/get_new_log_directory_by_process.sh $process_name`
# ../start_process/$process_name.sh
echo "Storing process info in '$log_path'"

process_id=`../start_process/$process_name.sh $log_path`

echo "Setting Process with name '$process_name' and id '$process_id'"
(cd ../../; python -m python.modules.processes.process_id set $process_name $process_id)

