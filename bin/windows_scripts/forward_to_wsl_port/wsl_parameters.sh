#!/usr/bin/bash
source ./scrape_comics_ports.sh # SCRAPE_COMICS_PORTS

WEB_SERVER_PORT=`../misc/get_config.sh ports.webServerPort`
IMAGE_HUB_PORT=`../misc/get_config.sh ports.imageHubPort`
PYTHON_HTTP_SERVER_PORT=`../misc/get_config.sh portsByProcess.pythonHttpServer`
NODE_SERVER_STATUS_PORT=`../misc/get_config.sh portsByProcess.nodeServerStatus`
WSL_SSH_PORT=2929
MONGO_PORT=27017

PI_ROBOT_PORTS=($WEB_SERVER_PORT $IMAGE_HUB_PORT $PYTHON_HTTP_SERVER_PORT $NODE_SERVER_STATUS_PORT $WSL_SSH_PORT $MONGO_PORT)

PORTS=(${PI_ROBOT_PORTS[@]})
PORTS+=(${SCRAPE_COMICS_PORTS[@]})

WSL_IP=`wsl hostname -I`
WINDOWS_IP='0.0.0.0'
# WINDOWS_IP=`ipconfig|grep -m 1 IPv4|sed "s/IPv4 Address. . . . . . . . . . . : //g" | xargs`

