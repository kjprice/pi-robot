#!/bin/bash
cd "$(dirname "$0")"
cd ..

gzip -c data/downloaded-images/image-raw.jpg | base64
