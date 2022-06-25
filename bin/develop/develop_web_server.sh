#!/bin/bash

cd "$(dirname "$0")"
source ../misc/setup_shell.sh

cd ../..

nodemon -e py -x './bin/run/run_web_server.sh'