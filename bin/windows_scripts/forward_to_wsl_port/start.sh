#!/usr/bin/bash
cd "$(dirname "$0")"

source ./wsl_parameters.sh

function run_on_port() {
    PORT=$1
    cmd="netsh interface portproxy add v4tov4 listenport=$PORT listenaddress=$WINDOWS_IP connectport=$PORT connectaddress=$WSL_IP"
    echo "Forwarding IP to WSL using the command:"
    echo $cmd
    echo
    echo `$cmd`
    echo 
}

for port in ${PORTS[@]}; do
    run_on_port $port
done