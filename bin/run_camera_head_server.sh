#!/bin/sh
cd "$(dirname "$0")"
cd ../python

# TODO: This is just temporary - find a better way to tie flask with the version of python we are actually using
if test -f "/Users/kjprice/anaconda3/envs/python3.6/bin/flask"; then
  alias flask=/Users/kjprice/anaconda3/envs/python3.6/bin/flask
fi

export FLASK_APP=run-camera-head.py
export PORT=9999
flask run --host=0.0.0.0 --port=$PORT