#!/bin/bash
cd "$(dirname "$0")"

cd ..

rsync -r --delete python pirobot:~/Projects/pirobot/
rsync -r --delete models pirobot:~/Projects/pirobot/