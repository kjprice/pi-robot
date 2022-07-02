#!/bin/bash

cd "$(dirname "$0")"
source ./setup_shell.sh

process_name=$1

process_id=`cd ../../; python -m python.modules.processes.process_id get $process_name`
if [ ! $process_id == -1 ]; then
  if ps -p $process_id > /dev/null; then
    echo "Found process running with id '$process_id', stopping process now."
    kill $process_id
  fi
  echo "Removing $process_name from processes store"
  `cd ../../; python -m python.modules.processes.process_id clear $process_name`
fi
