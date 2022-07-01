#!/bin/sh
filename=$1

if [ -f /usr/bin/tac ]; then
  reverse_command=tac # Linux
else
  reverse_command='tail -r' # Linux
fi

process_ids=$(ps aux | grep $filename | grep -v kill_process | awk '{print $2}' | $reverse_command)
echo $process_ids

# TODO: This file should find the process using "python -m python.modules.processes.process_id get"

echo "filename" "$filename"
i=0
for process_id in $process_ids; do
  ((i=i+1))
  echo $i

  if [ $i -ne 1 ]; then
    echo "killing $process_id"
    kill $process_id
  fi
done
