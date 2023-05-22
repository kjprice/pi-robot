#!/bin/bash
cd "$(dirname "$0")"

## Install Mongodb - requires 64bit OS
# https://www.mongodb.com/community/forums/t/add-mongodb-4-2-arm64-builds-for-raspberry-pi-os-64-bit-debian-buster/5046
# https://github.com/mongodb/mongo/blob/master/docs/building.md
# https://gist.github.com/kjprice/d233856093fd3a89fd19f1372aba7ba8
cd /tmp
sudo apt-get install -y gcc-10 g++-10
sudo apt-get install -y libssl-dev libcurl4-openssl-dev

git clone -b r4.4.0 https://github.com/mongodb/mongo.git
cd mongo


## Create python virtual environment for dependencies
python3 -m venv ~/.python_env/mongo_env
source ~/.python_env/mongo_env/bin/activate

python3 -m pip install -r etc/pip/compile-requirements.txt

time python3 buildscripts/scons.py install-core --disable-warnings-as-errors --ssl CC=/usr/bin/aarch64-linux-gnu-gcc-10 CXX=/usr/bin/aarch64-linux-gnu-g++-10 CCFLAGS="-march=armv8-a+crc -mtune=cortex-a72"

sudo cp build/install/bin/mongo* /usr/bin/
