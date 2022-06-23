#!/bin/bash
#### This is to help consolidate different python scripts so we always use the same version

# Needed for some non-interactive scripts (ie. "Windows Ubuntu WSL")
shopt -s expand_aliases

if test -f "/Users/kjprice/anaconda3/envs/python3.6/bin/python3.6"; then
  alias python=/Users/kjprice/anaconda3/envs/python3.6/bin/python3.6
elif [ -f /usr/bin/python3 ]; then
    alias python=/usr/bin/python3
fi