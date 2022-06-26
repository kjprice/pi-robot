#!/bin/bash

echo 
echo 
echo "### UPGRADING SYSTEM TOOLS"
echo 

# Make sure everything is up to date
sudo apt update
sudo apt -y full-upgrade
sudo apt-get update

source ~/.profile
