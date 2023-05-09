#!/usr/bin/bash

WEB_SERVER_PORT=`../misc/get_config.sh ports.webServerPort`
IMAGE_HUB_PORT=`../misc/get_config.sh ports.imageHubPort`
PYTHON_HTTP_SERVER_PORT=`../misc/get_config.sh portsByProcess.pythonHttpServer`
NODE_SERVER_STATUS_PORT=`../misc/get_config.sh portsByProcess.nodeServerStatus`
WSL_SSH_PORT=2929
MONGO_PORT=27017
COMIC_SCRAPE_PORT=9191

PORTS=($WEB_SERVER_PORT $IMAGE_HUB_PORT $PYTHON_HTTP_SERVER_PORT $NODE_SERVER_STATUS_PORT $WSL_SSH_PORT $MONGO_PORT $COMIC_SCRAPE_PORT)

WSL_IP=`wsl hostname -I`
WINDOWS_IP=`ipconfig|grep -m 1 IPv4|sed "s/IPv4 Address. . . . . . . . . . . : //g" | xargs`
