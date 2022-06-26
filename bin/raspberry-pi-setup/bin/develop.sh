#!/bin/bash
cd "$(dirname "$0")"
cd ..

nodemon -e sh,py -x "./bin/test_run.sh || true"