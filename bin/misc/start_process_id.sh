#!/bin/bash
set -e

cd "$(dirname "$0")"

./setup_shell.sh

process_name=$1
process_id=$2

echo "Received request to store new process with name '$process_name' and id '$process_id'"

old_process_id=`cd ../../; python -m python.modules.processes.process_id get $process_name`
if [ $old_process_id == -1 ]; then
  echo "Nothing to do"
else
  echo "Found process already running with id '$old_process_id', stopping old process now."
  ./kill $old_process_id
fi


echo "Setting new process '$process_name' with process id '$process_id'"
(cd ../../; python -m python.modules.processes.process_id set $process_name $process_id)