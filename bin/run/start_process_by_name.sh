#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh

process_name=$1

echo "Attempting to start new process with name '$process_name'"

old_process_id=`cd ../../; python -m python.modules.processes.process_id get $process_name`
if [ ! $old_process_id == -1 ]; then
  echo $process_name
  echo $old_process_id
  if ps -p $old_process_id > /dev/null; then
    echo "Found process already running with id '$old_process_id', stopping old process now."
    kill $old_process_id
  fi
  `cd ../../; python -m python.modules.processes.process_id set $process_name -1`
fi

log_path=`../misc/get_new_log_directory_by_process.sh $process_name`
# ../start_process/$process_name.sh
echo "Storing process info in '$log_path'"

process_id=`../start_process/$process_name.sh $log_path`

echo "Setting Process with name '$process_name' and id '$process_id'"
(cd ../../; python -m python.modules.processes.process_id set $process_name $process_id)

