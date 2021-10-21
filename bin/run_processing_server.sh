#!/bin/sh

# To run locally use (set LOCAL_PUB_SUB=true if also running camera head locally): nodemon -e py,sh -x 'LOCAL_PUB_SUB=true sh bin/run_processing_server.sh'

cd "$(dirname "$0")"
cd ../python

if test -f "/Users/kjprice/anaconda3/envs/python3.6/bin/python3.6"; then
  alias python3=/Users/kjprice/anaconda3/envs/python3.6/bin/python3.6
fi

python3 run_image_processing_server.py