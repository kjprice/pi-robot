#!/bin/sh
cd "$(dirname "$0")"
cd ../python

export FLASK_APP=run-servo-server.py
# lsof -ti tcp:5000 | xargs kill
flask run --host=0.0.0.0