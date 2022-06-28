#!/bin/bash

cd "$(dirname "$0")"

# TODO: When we initially setup the raspberry pi, set the PATH (maybe in .profile) so we don't have to do this here
node_folder=`(cd ~/.nvm/versions/node/**/bin/ && pwd)`
echo $node_folder
echo "Adding '$node_folder' to PATH"
PATH="$node_folder:$PATH"
node --version

echo "Starting server status server"
# ../../run/run_server_status_server.sh &

echo "starting python simple http server"
source ../../misc/setup_shell.sh
python_port=`../../misc/get_config.sh pythonFileSystemServerPort`
log_dir=`../../misc/get_config.sh logDirectoriesByProcess.pythonFileSystemDir`
../../misc/kill_process_on_port.sh $python_port
echo "Listening on port $python_port"
(cd ../../../data/ && python -m http.server $python_port >> $log_dir 2>&1 &)

exit 0