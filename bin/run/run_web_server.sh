#!/bin/bash

cd "$(dirname "$0")"
source ../misc/setup_shell.sh

# In case we want to pull images directly into the browser
# TODO: This path won't work
ln -s ~/Library/Projects/personal-misc/pi-robot/data/images ~/Library/Projects/personal-misc/pi-robot/static/

cd ../..

# TODO: Modules are not going to work, should run through main: `python -m python.main``
python python/pi_applications/web-app.py
