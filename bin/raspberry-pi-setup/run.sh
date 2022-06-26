#!/bin/bash
cd "$(dirname "$0")"

set -e

username=`./bin/get_config.sh username`
hostname=$1

./bin/validate_args.sh $hostname

./bin/copy_ssh_key.sh $hostname

./bin/send_setup_files.sh $hostname

./bin/run_setup_files.sh $hostname
