#!/bin/bash
cd "$(dirname "$0")"

WSL_IP=$1
PORT=$2
WINDOWS_IP=`ipconfig|grep -m 1 IPv4|sed "s/IPv4 Address. . . . . . . . . . . : //g" | xargs`

netsh interface portproxy delete v4tov4 listenport=$PORT listenaddress=$WINDOWS_IP