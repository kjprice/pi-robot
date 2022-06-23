#!/bin/bash
cd "$(dirname "$0")"
cd ..

nodemon -e py,sh -x "bash bin/run_tests.sh"
