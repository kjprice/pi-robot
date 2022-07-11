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

function find_newest_file_iterate() {
  path=$1
  sleep 0.1
  if [ -z $path ]; then
    echo ''
  elif [ -f $path ]; then
    echo "$path"
  else
    child_path=`ls $path/ | tail -n 1`
    if [ -z $child_path ]; then
      echo $path
    else
      most_recent_log=$path/$child_path
      find_newest_file_iterate $most_recent_log
    fi
  fi
}

path=`find_newest_file_iterate $folder_name`

if [ ! -f "$path" ]; then
  echo "process '$process_name' exists but no logs found in its directory '$folder_name'. Path found is '$path'" 1>&2
  exit 1
fi

echo "data/logs/$path"
cat "$path"
