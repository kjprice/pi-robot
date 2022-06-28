#!/bin/bash

cd "$(dirname "$0")"

# TODO: When we initially setup the raspberry pi, set the PATH (maybe in .profile) so we don't have to do this here
node_folder=`(cd ~/.nvm/versions/node/**/bin/ && pwd)`
echo $node_folder
echo "Adding '$node_folder' to PATH"
PATH="$node_folder:$PATH"
node --version

echo "Starting server status server"
../../run/run_server_status_server.sh &

echo "starting python simple http server"
../../run/run_python_filesystem_server.sh &

exit 0