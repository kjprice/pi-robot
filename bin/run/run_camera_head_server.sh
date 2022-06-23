#!/bin/sh

# To run locally: nodemon -e py,sh -x 'IS_TEST=true sh bin/run_camera_head_server.sh'
cd "$(dirname "$0")"

../misc/setup_shell.sh

filename=$(basename "$0")
../misc/kill_process_by_name.sh $filename

../download/download_model.sh

cd ../..

# TODO: Modules are not going to work, should run through main: `python -m python.main``
python python/pi_applications/run_camera_head_server.py
