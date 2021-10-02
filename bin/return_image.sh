#!/bin/bash
cd "$(dirname "$0")"
cd ..

# We need to make a copy of the image, otherwise the image might be corrupted as it is overwritten
cp data/images/image-raw.jpg data/images/image-raw-safe.jpg
gzip -c data/images/image-raw-safe.jpg | base64
