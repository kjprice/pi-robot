#!/bin/bash
cd "$(dirname "$0")"

cd ../..

# raspberry pi (robot)
rsync -r --delete python pirobot:~/Projects/pirobot/
rsync -r --delete bin pirobot:~/Projects/pirobot/

# raspberry pi (misc)
rsync -r --delete python pi3misc:~/Projects/pirobot/
rsync -r --delete bin pi3misc:~/Projects/pirobot/

# raspberry pi (misc)
# rsync -r --delete python pi@pi3misc2:~/Projects/pirobot/
rsync -r --delete bin pi@pi3misc2:~/Projects/pirobot/
