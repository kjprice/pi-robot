#!/bin/bash
cd "$(dirname "$0")"

libcamera-vid -t 0 --inline --listen -o tcp://0.0.0.0:11155

# time libcamera-still -t 1000 -o test%d.jpg --timelapse 100
