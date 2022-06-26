#!/bin/bash
cd "$(dirname "$0")"
cd ..

config_name=$1

function get_config()
{
    filename=$1
    # echo $filename
    filepath="config/$filename.txt"
    cat $filepath
}

case $config_name in
"username")
    get_config 'pi_username'
;;
"setup_filepath")
    get_config 'setup_filepath'
esac