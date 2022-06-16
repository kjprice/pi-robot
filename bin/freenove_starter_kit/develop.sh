#!/bin/bash
cd "$(dirname "$0")"

nodemon -w ../.. -e py -x 'sh run_freenove.sh'