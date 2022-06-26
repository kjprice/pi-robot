#!/bin/bash

cd "$(dirname "$0")"

echo 
echo 
echo "### Creating Startup Script"
echo 

src=./init.d/robot_startup.sh
destination=/etc/init.d/robot_startup
sudo cp $src $destination
sudo update-rc.d robot_startup defaults
