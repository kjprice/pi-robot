#!/usr/bin/bash
cd "$(dirname "$0")"

WSL_IP=`wsl hostname -I`
PORT=`../misc/get_config.sh ports.webServerPort`

WINDOWS_IP=`ipconfig|grep -m 1 IPv4|sed "s/IPv4 Address. . . . . . . . . . . : //g" | xargs`

cmd="netsh interface portproxy delete v4tov4 listenport=$PORT listenaddress=$WINDOWS_IP"
echo "Canceling IP Forward to WSL using the command:"
echo $cmd
echo
echo `$cmd`

