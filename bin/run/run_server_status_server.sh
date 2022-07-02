#!/bin/bash

cd "$(dirname "$0")"

port=`../misc/get_config.sh ports.healthStatusPort`

source ../misc/setup_shell.sh

../misc/kill_process_on_port.sh $port > /dev/null

cd ../../nodejs/server_status/

log_filepath=$1

npm install >> ../../$log_filepath 2>&1

node index >> ../../$log_filepath 2>&1 &

process_id="$!"

echo $process_id