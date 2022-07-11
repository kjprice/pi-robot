#!/bin/bash

cd "$(dirname "$0")"

port=`../misc/get_config.sh portsByProcess.nodeServerStatus`

source ../misc/setup_shell.sh

../misc/kill_process_on_port.sh $port

cd ../../nodejs/server_status/

log_filepath=$1

npm install
node index 
