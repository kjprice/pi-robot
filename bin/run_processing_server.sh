#!/bin/sh

# To run locally use (set LOCAL_PUB_SUB=true if also running camera head locally): nodemon -e py,sh -x 'LOCAL_PUB_SUB=true sh bin/run_processing_server.sh'

cd "$(dirname "$0")"
cd ../python

# export IS_TEST=true
# TODO: This is just temporary - find a better way to tie flask with the version of python we are actually using
alias flask=/Users/kjprice/anaconda3/envs/python3.6/bin/flask

export FLASK_APP=run-image-processing-server.py
# lsof -ti tcp:5000 | xargs kill
export PORT=5000
flask run --host=0.0.0.0 --port=$PORT