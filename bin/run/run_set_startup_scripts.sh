#!/bin/bash

# This sets all startup scripts
# TODO: This should be done in a init.d file: https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#init

cd "$(dirname "$0")"

servers=`../misc/get_config.sh servers`

../misc/copy.sh

for server in ${servers[@]}
do
  : 
  echo "# $server"
  # TODO: Use a symbolic link to the script
  ssh -o ConnectTimeout=5 pi@$server '~/Projects/pirobot/bin/on_pi_startup/set_startup_script.sh'
  echo
done