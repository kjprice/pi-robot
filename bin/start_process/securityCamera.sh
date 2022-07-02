#!/bin/bash

cd "$(dirname "$0")"

log_path=$1

../misc/setup_shell.sh

../run/run_security_camera_forever.sh >> ../../$log_path 2>&1 &

process_id="$!"

echo $process_id