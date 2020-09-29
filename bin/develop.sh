#!/bin/bash
cd "$(dirname "$0")"
cd ../python

source ~/.bash_profile
ca

script_to_run=servo-module.py
# script_to_run=process-image-for-servo.py

nodemon -e py,sh -x "time python $script_to_run"
