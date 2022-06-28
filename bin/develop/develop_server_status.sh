#!/bin/bash
cd "$(dirname "$0")"
cd ../..

nodemon -e py,sh -x "./bin/run/run_server_status_server.sh"
