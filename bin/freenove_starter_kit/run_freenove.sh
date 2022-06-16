#!/bin/bash
cd "$(dirname "$0")"
cd ../..

# This gets run locally
scp -r python/freenove pi3misc2:~/Projects/pirobot/python/

ssh pi3misc2 'sh ~/Projects/pirobot/bin/kill_process_by_name.sh freenove &> /dev/null'
ssh pi3misc2 'python ~/Projects/pirobot/python/freenove/main.py'