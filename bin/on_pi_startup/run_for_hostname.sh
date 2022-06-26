#!/bin/bash

cd "$(dirname "$0")"

# TODO: Add to config
LOGS_DIR=../../data/logs/startup
mkdir -p $LOGS_DIR
log_filename=$(date '+%Y-%m-%d_%H_%M_%S').txt
log_filepath=$LOGS_DIR/$log_filename


filepath=startup_by_hostname/`hostname`.sh

if [ -f $filepath ]; then
  echo "Running startup file $filepath"
  (exec ./$filepath || true | tee $log_filepath) &
  echo "Finished"
  echo
fi