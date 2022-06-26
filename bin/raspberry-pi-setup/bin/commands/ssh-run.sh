#!/bin/bash
cd "$(dirname "$0")"
cd ../..

# Runs a commmand via ssh

username=`./bin/get_config.sh username`
hostname="$1"
command="$2"

echo "ssh $username@$hostname '$command'"