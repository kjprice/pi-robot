#!/usr/bin/bash
cd "$(dirname "$0")"
source ../misc/setup_shell.sh

cd ../..


nodemon -e sh -x 'bash ./bin/windows_scripts/forward_to_wsl_port/start.sh'
