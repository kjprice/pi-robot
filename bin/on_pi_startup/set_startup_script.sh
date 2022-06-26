#!/bin/bash

cd "$(dirname "$0")"

# check if we are already running file in rc.local
# if not then append to file
# TODO: This should be done in init.d, revert rc.local once that is done

startup_file='/etc/rc.local'
search_text="# PIROBOT_STARTUP"

BACKUPS_DIR=~/.backups/$startup_file

if ! grep -Fxq "$search_text" $startup_file
then
    echo "Creating backup of $startup_file"
    mkdir -p $BACKUPS_DIR
    backup_filename=$(date '+%Y-%m-%d_%H_%M_%S')
    backup_filepath=$BACKUPS_DIR/$backup_filename
    cp $startup_file $backup_filepath

    echo "Adding startup script"

    # get the current directory
    dir=`pwd`
    script_filepath=$dir/run_for_hostname.sh

    # Script will always exit without an error
    script="$script_filepath || true &"

    echo $search_text | sudo tee -a $startup_file
    echo $script | sudo tee -a $startup_file
fi