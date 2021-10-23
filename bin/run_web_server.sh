#!/bin/sh

cd "$(dirname "$0")"
cd ../python

source ~/.bash_profile
ca

# In case we want to pull images directly into the browser
ln -s /Users/kjprice/Library/Projects/personal-misc/pi-robot/data/images /Users/kjprice/Library/Projects/personal-misc/pi-robot/static/

nodemon -e py -x 'python3.6 web-app.py'