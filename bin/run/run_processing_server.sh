#!/bin/bash

# To run locally use (set LOCAL_PUB_SUB=true if also running camera head locally): nodemon -e py,sh -x 'LOCAL_PUB_SUB=true sh bin/run_processing_server.sh'

cd "$(dirname "$0")"
source ../misc/setup_shell.sh

cd ../..

# TODO: Modules are not going to work, should run through main: `python -m python.main``
python python/pi_applications/run_image_processing_server.py