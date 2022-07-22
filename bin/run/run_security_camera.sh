#!/bin/bash

cd "$(dirname "$0")"

cd ../..

# TODO: Delete thsi file if not needed
# How many seconds each video should capture
SECONDS=30
MS=$(expr $SECONDS*1000 | bc)

filename=$(date '+%Y-%m-%d_%H_%M_%S')
folder=$(date '+%Y-%m-%d')


DATA_DIR=data/security_videos/$folder
mkdir -p $DATA_DIR

filename=$(date '+%Y-%m-%d_%H_%M_%S')
raw_filepath=$DATA_DIR/$filename.h264
mp4_filepath=$DATA_DIR/$filename.mp4


# Take video transformed to mp4
# TODO: Don't log everything
# TODO: Stream video out for a browser
time libcamera-vid -t $MS -o $raw_filepath
time MP4Box -add $raw_filepath $mp4_filepath

rm $raw_filepath