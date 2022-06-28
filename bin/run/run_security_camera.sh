#!/bin/bash

cd "$(dirname "$0")"

cd ../..

# How many seconds each video should capture
SECONDS=1
MS=$(expr $SECONDS*1000 | bc)

filename=$(date '+%Y-%m-%d_%H_%M_%S')
folder=$(date '+%Y-%m-%d')


DATA_DIR=data/security_videos/$folder
LOGS_DIR=data/logs/security_videos
mkdir -p $DATA_DIR
mkdir -p $LOGS_DIR

filename=$(date '+%Y-%m-%d_%H_%M_%S')
raw_filepath=$DATA_DIR/$filename.h264
mp4_filepath=$DATA_DIR/$filename.mp4

ALL_LOGS_FILEPATH=$LOGS_DIR/all.txt

THIS_LOG_FILEPATH=$LOGS_DIR/video_$filename.txt

# Take video transformed to mp4
time libcamera-vid -t $MS -o $raw_filepath |& tee -a $ALL_LOGS_FILEPATH $THIS_LOG_FILEPATH
time MP4Box -add $raw_filepath $mp4_filepath |& tee -a $ALL_LOGS_FILEPATH $THIS_LOG_FILEPATH

rm $raw_filepath