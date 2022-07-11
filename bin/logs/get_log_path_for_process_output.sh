#!/bin/bash

cd "$(dirname "$0")"

source ../misc/setup_shell.sh

process_name=$1

if [ -z $process_name ]; then
  echo "process_name is a required argument" 1>&2
  exit 1
fi

process_log_dir_name=`../misc/get_config.sh logDirectoriesByProcess.$process_name`

year=$(date '+%Y')
month=$(date '+%m')
day=$(date '+%d')
hour=$(date '+%H')
log_filename=$hour.txt
# log_filename=$(date '+%Y-%m-%d_%H_%M_%S').txt
log_dir=data/logs/$process_log_dir_name/$year/$month/$day
mkdir -p ../../$log_dir
# log_path=$log_dir/$log_filename
log_path=$log_dir/$hour

echo $log_path