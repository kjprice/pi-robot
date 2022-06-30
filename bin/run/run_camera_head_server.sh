#!/bin/bash

# To run locally: nodemon -e py,sh -x 'IS_TEST=true sh bin/run_camera_head_server.sh'
cd "$(dirname "$0")"

source ../misc/setup_shell.sh

# filename=$(basename "$0")
# ../misc/kill_process_by_name.sh $filename

../download/download_model.sh

cd ../..

if [ -z $IS_TEST ] ; then
    python -m python.pi_applications.run_camera_head_server $@
else
    python -m python.pi_applications.run_camera_head_server --is_test
fi