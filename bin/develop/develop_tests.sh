#!/bin/bash
cd "$(dirname "$0")"
cd ../..

nodemon -e py,sh -x "bash bin/run/run_tests.sh"
