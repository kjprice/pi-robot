#!/bin/bash

cd "$(dirname "$0")"

log_path=$1

../misc/setup_shell.sh

../run/run_server_status_server.sh $log_path

process_id="$!"
echo $process_id
