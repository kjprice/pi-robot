#!/usr/bin/bash
cd "$(dirname "$0")"

cd ../../..
python -m python.modules.get_config_value -k $1