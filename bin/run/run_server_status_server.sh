#!/bin/bash

cd "$(dirname "$0")"

port=`../misc/get_config.sh healthStatusPort`

../misc/kill_process_on_port.sh $port

cd ../../nodejs/server_status/

# TODO: Add log directory to config
LOGS_DIR=../../data/logs/node_server_status
mkdir -p $LOGS_DIR
log_filename=$(date '+%Y-%m-%d_%H_%M_%S').txt
log_filepath=$LOGS_DIR/$log_filename

npm install >> $log_filepath 2>&1

node index >> $log_filepath 2>&1 &