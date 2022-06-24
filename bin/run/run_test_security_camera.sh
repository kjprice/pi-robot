cd "$(dirname "$0")"
cd ../

rm -r ../data/security_videos

./misc/copy.sh
ssh pi@pi3misc2 'bash ~/Projects/pirobot/bin/run/run_security_camera.sh'
./download/download_security_videos.sh
