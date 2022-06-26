#!/bin/bash
set -e # Exit if any errors
cd "$(dirname "$0")"
cd ../..

source ./bin/misc/setup_shell.sh

echo "Running raspberry-pi-setup tests"
./bin/raspberry-pi-setup/bin/test_run.sh
echo
echo

python -m python.tests