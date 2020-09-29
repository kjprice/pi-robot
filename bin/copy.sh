#!/bin/bash
cd "$(dirname "$0")"

cd ..

rsync -r python pirobot:~/Projects/pirobot/
rsync -r models pirobot:~/Projects/pirobot/