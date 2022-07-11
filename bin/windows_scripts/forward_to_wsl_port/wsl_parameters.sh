#!/usr/bin/bash

WEB_SERVER_PORT=`../misc/get_config.sh ports.webServerPort`
IMAGE_HUB_PORT=`../misc/get_config.sh ports.imageHubPort`
PYTHON_HTTP_SERVER_PORT=`../misc/get_config.sh portsByProcess.pythonHttpServer`
NODE_SERVER_STATUS_PORT=`../misc/get_config.sh portsByProcess.nodeServerStatus`

PORTS=($WEB_SERVER_PORT $IMAGE_HUB_PORT $PYTHON_HTTP_SERVER_PORT $NODE_SERVER_STATUS_PORT)

WSL_IP=`wsl hostname -I`
WINDOWS_IP=`ipconfig|grep -m 1 IPv4|sed "s/IPv4 Address. . . . . . . . . . . : //g" | xargs`
