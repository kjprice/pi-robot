#!/bin/bash
cd "$(dirname "$0")"
cd ../..

# Creates scp command

username=`./bin/get_config.sh username`
hostname="$1"
src_file="$2"
destination_path="$3"

echo "scp $src_file $username@$hostname:$destination_path"