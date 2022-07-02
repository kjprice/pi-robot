#!/bin/bash
cd "$(dirname "$0")"
cd ../..

# This gets run locally
scp -r bin/test_camera/test_camera.sh pi3misc2:~/Projects/pirobot/bin/

ssh pi3misc2 'bash ~/Projects/pirobot/bin/test_camera.sh'

scp -r pi3misc2:/tmp/test_camera/ data/