#!/bin/bash
cd "$(dirname "$0")"

process_name=$1
error_flag=$2


while read LINE; do
  log_path=`./get_log_path_for_process_output.sh $process_name`
  if [ "$error_flag" = 'error' ]; then
    log_path=$log_path.error.txt
  else
    log_path=$log_path.txt
  fi
  echo "${LINE}" >> ../../$log_path
done