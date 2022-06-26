#!/bin/bash
cd "$(dirname "$0")"
cd ..

hostname=$1

./bin/validate_args.sh $hostname

help_message=`cat text/ssh-run-setup-files.txt`
setup_path=`./bin/get_config.sh setup_filepath`
echo "$help_message"

cmd_server="sh $setup_path/initial_setup.sh"
cmd=`./bin/commands/ssh-run.sh $hostname "$cmd_server"`

./bin/run_command.sh "$cmd"