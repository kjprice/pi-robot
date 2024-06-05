#!/bin/bash
cd "$(dirname "$0")"

echo 
echo 
echo "### Things needed for a fresh ubuntu wsl on Windows"
echo 

# install utilities common with raspberry pi
./common_dependencies.sh

sudo apt update
sudo apt -y full-upgrade
sudo apt-get update

echo 'PATH=$PATH:~/.local/bin/' >> ~/.bash_profile

source ~/.bash_profile

sudo apt install python3-pip

python3 -m pip install --no-input imagezmq
python3 -m pip install --no-input psutil
python3 -m pip install --no-input bs4 # Beautiful Soup
# python3 -m pip install --no-input jupyterlab
# python3 -m pip install --no-input notebook
python3 -m pip install --no-input matplotlib
python3 -m pip install --no-input tensorflow
python3 -m pip install --no-input keras

# Install Cuda and Ananconda https://docs.microsoft.com/en-us/windows/ai/directml/gpu-tensorflow-wsl
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
bash Miniconda3-latest-Linux-x86_64.sh 

# May need to open new terminal
conda create --name directml python=3.6 
conda activate directml 

pip install tensorflow-directml

conda install ipykernel
ipython kernel install --user --name=directml

# TO start ssh on wsl ubuntu:
# - sudo service ssh start
# - See /README.md on how to automatically start ssh on wsl

# MongoDB
# https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-database

cd ~
sudo apt update
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
mkdir -p ~/data/db

# TO verify mongo is running
# sudo mongod --dbpath ~/data/db
# ps -e | grep 'mongod'

# Have MongoDB start automatically
curl https://raw.githubusercontent.com/mongodb/mongo/master/debian/init.d | sudo tee /etc/init.d/mongodb >/dev/null
sudo chmod +x /etc/init.d/mongodb
sudo service mongodb start 
