cd "$(dirname "$0")"
cd ../

nodemon -e py,sh -x "./run/run_test_security_camera.sh"
