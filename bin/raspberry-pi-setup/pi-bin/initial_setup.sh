#!/bin/bash
cd "$(dirname "$0")"

./step1_upgrade.sh

# Create Projects Folder
mkdir -p ~/Projects/pirobot

./step2_install_depencies.sh

echo 
echo 'Setup is complete!!'