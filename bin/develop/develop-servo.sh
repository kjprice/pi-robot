#!/bin/bash
cd "$(dirname "$0")"
cd ../..

source ~/.bash_profile
ca

nodemon -e py,sh -x "time IS_TEST=true ./bin/run/run_servo_server.sh"
