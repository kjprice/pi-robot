#!/bin/bash
cd "$(dirname "$0")"
cd ../..

# Creates ssh-copy-id command

username=`./bin/get_config.sh username`
hostname="${@: -1}" # Last arg

echo "ssh-copy-id $username@$hostname"