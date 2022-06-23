#!/bin/bash
cd "$(dirname "$0")"
cd ..

#### This is to help consolidate different python scripts so we always use the same version

# Needed for some non-interactive scripts (ie. "Windows Ubuntu WSL")
shopt -s expand_aliases

if [ -f /usr/bin/python3 ]; then
    alias python=/usr/bin/python3
fi