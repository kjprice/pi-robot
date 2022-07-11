#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh

process_name=$1
other_args=$2

echo "Attempting to start new process with name '$process_name'"

../misc/kill_process_by_name.sh $process_name

({ ../start_process/$process_name.sh "$other_args" 2>&3 | ../logs/write_std_log.sh $process_name; } 3>&1 | ../logs/write_std_log.sh $process_name error ) &

process_id="$!"

echo "Setting Process with name '$process_name' and id '$process_id'"
(cd ../../; python -m python.modules.processes.process_id set $process_name $process_id)

