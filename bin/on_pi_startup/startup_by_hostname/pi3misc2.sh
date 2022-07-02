#!/bin/bash

cd "$(dirname "$0")"

./all.sh

../../run/start_process_by_name.sh securityCamera
