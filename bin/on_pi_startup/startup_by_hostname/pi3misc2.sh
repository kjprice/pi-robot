#!/bin/bash

cd "$(dirname "$0")"

./all.sh

../../run/run_security_camera_forever.sh &