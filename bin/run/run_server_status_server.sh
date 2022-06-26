#!/bin/bash

cd "$(dirname "$0")"

port=`../misc/get_config.sh health_status_port`

../misc/kill_process_on_port.sh $port

cd ../../nodejs/server_status

npm install

echo "Running server status server on port $port"
node index &