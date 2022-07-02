#!/usr/bin/bash
cd "$(dirname "$0")"

WSL_IP=`wsl hostname -I`
WEB_SERVER_PORT=`../misc/get_config.sh ports.webServerPort`
IMAGE_HUB_PORT=`../misc/get_config.sh ports.imageHubPort`

WINDOWS_IP=`ipconfig|grep -m 1 IPv4|sed "s/IPv4 Address. . . . . . . . . . . : //g" | xargs`

function run_on_port() {
    PORT=$1
    cmd="netsh interface portproxy add v4tov4 listenport=$PORT listenaddress=$WINDOWS_IP connectport=$PORT connectaddress=$WSL_IP"
    echo "Forwarding IP to WSL using the command:"
    echo $cmd
    echo
    echo `$cmd`
    echo 
}

run_on_port $WEB_SERVER_PORT
run_on_port $IMAGE_HUB_PORT
