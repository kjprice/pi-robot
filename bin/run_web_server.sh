#!/bin/sh

cd "$(dirname "$0")"
cd ../python

source ~/.bash_profile
ca

nodemon -e py -x 'python3.6 web-app.py'