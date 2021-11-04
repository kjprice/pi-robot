#!/bin/sh

# To run locally: nodemon -e py,sh -x 'IS_TEST=true sh bin/run_camera_head_server.sh'
cd "$(dirname "$0")"

./download_model.sh
cd ../python


if test -f "/Users/kjprice/anaconda3/envs/python3.6/bin/python3.6"; then
  alias python3=/Users/kjprice/anaconda3/envs/python3.6/bin/python3.6
fi


filename=$(basename "$0")
./kill_process_by_name.sh $filename

python3 run_camera_head_server.py