#!/bin/bash
cd "$(dirname "$0")"

echo 
echo 
echo "### INSTALLING DEPENCIES"
echo 

# install utilities common with wsl
../common_dependencies.sh

# Taken from https://ai-pool.com/d/how-to-install-keras-on-raspberry-pi-
# ML Libraries
sudo apt-get install -y python3-numpy
sudo apt-get install -y libblas-dev
sudo apt-get install -y liblapack-dev
sudo apt-get install -y python3-dev
sudo apt-get install -y gfortran
sudo apt-get install -y python3-setuptools
sudo apt-get update
sudo apt-get install -y python3-h5py
sudo apt-get install -y vim

# PiCamera2 dependencies
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg

# Install common ML libraries
sudo apt-get install -y python3-scipy
python3 -m pip install scipy
python3 -m pip install cython
python3 -m pip install --user -U nltk

# TODO: install tensorflow lite: https://lindevs.com/install-precompiled-tensorflow-lite-on-raspberry-pi/
# TODO: install keras

# Raspberry Pi Camera for Python
python3 -m pip install --no-input numpy --upgrade
python3 -m pip install --no-input picamera2

# Video encoders
sudo apt install -y gpac # MP4 Format

# Google Drive
pip install --no-input --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Webmin
# https://pimylifeup.com/raspberry-pi-webmin/
sudo apt-get install -y perl libnet-ssleay-perl openssl libauthen-pam-perl libpam-runtime libio-pty-perl apt-show-versions shared-mime-info
cd /tmp
wget http://prdownloads.sourceforge.net/webadmin/webmin_1.994_all.deb
sudo dpkg --install webmin_1.994_all.deb


# Instructions from Freenove
# https://drive.google.com/file/d/16ximR2Ka6HJDdu20Xr7_sWo04teDhlcP/view
cd /tmp
git clone https://github.com/WiringPi/WiringPi
cd WiringPi
./build

## Freenove code
cd ~
mkdir -p kits

cd ~/kits
git clone --depth 1 https://github.com/freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi
mv Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/ Freenove_Kit/

cd ~/kits
git clone https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi Freenove_Robot_Dog


cd /tmp/setup
./mongo/install_mongo.sh