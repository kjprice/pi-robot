#!/bin/bash
cd "$(dirname "$0")"

process_name=$1

folder_name=`../misc/get_config.sh logDirectoriesByProcess.$process_name`

if [ -z $folder_name ] || [ $folder_name == null ]; then
  echo "No log folder found by the process name '$process_name'" 1>&2
  exit 1
fi


cd ../../data/logs/

if [ ! -d "$folder_name/" ]; then
  echo "process '$process_name' exists but its directory '$folder_name' is not created yet" 1>&2
  exit 1
fi

most_recent_log=`ls $folder_name/ | tail -n 1`

if [ ! -f "$folder_name/$most_recent_log" ]; then
  echo "process '$process_name' exists but no logs found in its directory '$folder_name'" 1>&2
  exit 1
fi

echo "$folder_name/$most_recent_log"
cat "$folder_name/$most_recent_log"
