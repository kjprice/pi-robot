#!/bin/bash

# To run locally use (set LOCAL_PUB_SUB=true if also running camera head locally): nodemon -e py,sh -x 'LOCAL_PUB_SUB=true sh bin/run_processing_server.sh'

cd "$(dirname "$0")"
source ../misc/setup_shell.sh

cd ../..

python -m python.pi_applications.run_image_processing_server