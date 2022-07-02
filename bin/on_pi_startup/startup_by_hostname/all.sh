#!/bin/bash

cd "$(dirname "$0")"

# TODO: When we initially setup the raspberry pi, set the PATH (maybe in .profile) so we don't have to do this here
node_folder=`(cd ~/.nvm/versions/node/**/bin/ && pwd)`
echo $node_folder
echo "Adding '$node_folder' to PATH"
PATH="$node_folder:$PATH"
node --version

source ../../misc/setup_shell.sh

echo "Clearing all stored process ids"
( cd ../../../; python -m python.modules.processes.process_id clear )

echo "Starting server status server"
# ../../run/run_server_status_server.sh &
../../run/start_process_by_name.sh nodeServerStatus

echo "starting python simple http server"
../../run/start_process_by_name.sh pythonHttpServer

exit 0