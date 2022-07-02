#!/bin/bash
cd "$(dirname "$0")"
cd ../data/images/images-captured

# Get the newest image
img_to_pull=$(ls -t | head -n 1)

# Zip and then encode so that python can digest a string of recognizable characters
# TODO: Make sure that zipping the file is worth it (trade of CPU versus network speed0)
gzip -c $img_to_pull | base64
