#!/bin/bash
cd "$(dirname "$0")"

source ~/.profile
python3 -m pip install gdown
source ~/.profile

gdown 'https://drive.google.com/uc?id=1CnNH_d-QcWOZW2ehOjEP0sTcFQg-O3X1'

unzip -o mongobin.zip
mv mongobin/mongo* /usr/bin/