#!/usr/bin/bash
cd "$(dirname "$0")"

source ./wsl_parameters.sh

function kill_on_port() {
    PORT=$1
    cmd="netsh interface portproxy delete v4tov4 listenport=$PORT listenaddress=$WINDOWS_IP"
    echo "Canceling IP Forward to WSL using the command:"
    echo $cmd
    echo
    echo `$cmd`
    echo
}

for port in ${PORTS[@]}; do
    kill_on_port $port
done