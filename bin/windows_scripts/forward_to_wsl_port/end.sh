#!/usr/bin/bash
cd "$(dirname "$0")"

WSL_IP=`wsl hostname -I`
WEB_SERVER_PORT=`../misc/get_config.sh ports.webServerPort`
IMAGE_HUB_PORT=`../misc/get_config.sh ports.imageHubPort`
PYTHON_HTTP_SERVER_PORT=`../misc/get_config.sh portsByProcess.pythonHttpServer`
NODE_SERVER_STATUS_PORT=`../misc/get_config.sh portsByProcess.nodeServerStatus`

WINDOWS_IP=`ipconfig|grep -m 1 IPv4|sed "s/IPv4 Address. . . . . . . . . . . : //g" | xargs`

function kill_on_port() {
    PORT=$1
    cmd="netsh interface portproxy delete v4tov4 listenport=$PORT listenaddress=$WINDOWS_IP"
    echo "Canceling IP Forward to WSL using the command:"
    echo $cmd
    echo
    echo `$cmd`
    echo
}

kill_on_port $WEB_SERVER_PORT
kill_on_port $IMAGE_HUB_PORT
kill_on_port $PYTHON_HTTP_SERVER_PORT
kill_on_port $NODE_SERVER_STATUS_PORT