#!/bin/bash
cd "$(dirname "$0")"
cd ..

hostname=$1

./bin/validate_args.sh $hostname

help_message=`cat text/ssh-copy-id-text.txt`
echo "$help_message"



cmd=`./bin/commands/ssh-copy-id.sh $hostname`

./bin/run_command.sh "$cmd"