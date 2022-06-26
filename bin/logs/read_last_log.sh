#!/bin/bash

cd "$(dirname "$0")"

log_directory_name=$1

cd ../../data/logs/
most_recent_log=`ls $log_directory_name/ | tail -n 1`

echo $most_recent_log

cat $log_directory_name/$most_recent_log
