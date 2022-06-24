#!/bin/bash
cd "$(dirname "$0")"
DATA_DIR=data/security_videos
cd ../..

# mkdir -p $DATA_DIR

scp -r pi@pi3misc2:~/Projects/pirobot/$DATA_DIR/ data/