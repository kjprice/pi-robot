#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh

process_name=$1

log_dir=`../misc/get_config.sh logDirectoriesByProcess.$process_name`

log_filename=$(date '+%Y-%m-%d_%H_%M_%S').txt
log_dir=data/logs/$log_dir
mkdir -p ../../$log_dir
log_path=$log_dir/$log_filename

echo $log_path

# TODO: MOve this file to bin/logs
# TODO: Make logging smarter so that folders are grouped by day, would require some rewrite