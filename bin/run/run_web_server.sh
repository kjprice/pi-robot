#!/bin/bash

cd "$(dirname "$0")"
source ../misc/setup_shell.sh

# In case we want to pull images directly into the browser
# TODO: This path won't work
# ln -s ~/Library/Projects/personal-misc/pi-robot/data/images ~/Library/Projects/personal-misc/pi-robot/static/

cd ../..

python -m python.web_app
