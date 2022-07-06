#!/bin/bash
#### This is to help consolidate different node/python scripts so we always use the same version

# Needed for some non-interactive scripts (ie. "Windows Ubuntu WSL")
shopt -s expand_aliases

function get_first_word() {
  cat - | head -1 | awk '{print $1}'
}

function get_nvm_bin_filepath() {
  nvm_node_folder=~/.nvm/versions/node
  if [ -d $nvm_node_folder ]; then
    version=`ls "$nvm_node_folder" | get_first_word`
    path=$nvm_node_folder/$version/bin
    echo $path
  fi
}

function setup_node() {
  node_path=`get_nvm_bin_filepath`
  if [ ! -z $node_path ]; then
    PATH="$PATH:$node_path"
  fi
}

function setup_python() {
  if test -f "/Users/kjprice/anaconda3/envs/python3.6/bin/python3.6"; then
    alias python=/Users/kjprice/anaconda3/envs/python3.6/bin/python3.6
  elif [ -f /usr/bin/python3 ]; then
      alias python=/usr/bin/python3
  fi
}

setup_node
setup_python