#!/usr/bin/bash
cd "$(dirname "$0")"

WSL_IP=`wsl hostname -I`
PORT=9898 # TODO: Pull from config.json

WINDOWS_IP=`ipconfig|grep -m 1 IPv4|sed "s/IPv4 Address. . . . . . . . . . . : //g" | xargs`

cmd="netsh interface portproxy add v4tov4 listenport=$PORT listenaddress=$WINDOWS_IP connectport=$PORT connectaddress=$WSL_IP"
echo "Forwarding IP to WSL using the command:"
echo $cmd
echo
echo `$cmd`
