#!/bin/bash
cd "$(dirname "$0")"
cd ../../

# nodemon -e py,sh -x "./run/run_test_security_camera.sh"
nodemon -e py,sh -x "python -m python.modules.get_config_value || true"