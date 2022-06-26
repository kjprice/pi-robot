#!/bin/bash
cd "$(dirname "$0")"
cd ../..

# Creates scp command

username=`./bin/get_config.sh username`
hostname="$1"
src_dir="$2"
destination_path="$3"

echo "rsync -r $src_dir $username@$hostname:$destination_path"