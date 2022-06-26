#!/bin/bash
cd "$(dirname "$0")"
cd ..

hostname=$1

./bin/validate_args.sh $hostname

help_message=`cat text/ssh-scp-setup-files.txt`
setup_path=`./bin/get_config.sh setup_filepath`
echo "$help_message"

cmd=`./bin/commands/scp.sh $hostname pi-bin/ $setup_path`
./bin/run_command.sh "$cmd"