#!/bin/bash
cd "$(dirname "$0")"
DATA_DIR=data/security_videos
cd ../..

rsync -r pi@pi3misc2:~/Projects/pirobot/$DATA_DIR data/