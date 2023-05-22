#!/bin/bash
cd "$(dirname "$0")"
sudo chown root:root /usr/bin/mongo*
sudo chmod 755 /usr/bin/mongo*

sudo cp /tmp/setup/mongo/mongod.service /lib/systemd/system/mongodb.service
sudo cp /tmp/setup/mongo/mongodb.conf /etc/mongodb.conf
sudo adduser --no-create-home --disabled-login --disabled-password --gecos "" mongodb

sudo mkdir -p /var/log/mongodb/
sudo chown -R mongodb:mongodb /var/log/mongodb/
sudo mkdir /data
sudo chmod 777 /data
sudo mkdir -p /data/db
sudo chown -R mongodb:mongodb /data/db

# sudo systemctl daemon-reload && sudo systemctl start mongodb.service ; systemctl status mongodb.service
sudo systemctl start mongodb.service
sudo systemctl status mongodb.service