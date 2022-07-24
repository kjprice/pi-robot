#!/bin/bash
cd "$(dirname "$0")"

nodemon -e sh -x 'sh run_test_video.sh || true'
# nodemon -e sh -x 'sh run_test_camera.sh'
