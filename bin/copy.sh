#!/bin/bash
cd "$(dirname "$0")"

cd ..

scp -r python/ pirobot:~/Projects/pirobot