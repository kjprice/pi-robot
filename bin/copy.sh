#!/bin/bash
cd "$(dirname "$0")"

cd ..

# raspberry pi (robot)
rsync -r --delete python pirobot:~/Projects/pirobot/
rsync -r --delete models pirobot:~/Projects/pirobot/

# raspberry pi (misc)
rsync -r --delete python pi3misc:~/Projects/pirobot/
rsync -r --delete bin pi3misc:~/Projects/pirobot/
