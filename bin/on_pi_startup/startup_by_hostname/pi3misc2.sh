#!/bin/bash

cd "$(dirname "$0")"

./all.sh

../../run/run_security_camera_forever.sh &
# TODO: Set process id here similar to how it is done in run_python_filesystem_server.sh