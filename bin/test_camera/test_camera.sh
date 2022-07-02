# This is ran on the raspberry pi

data_dir=/tmp/test_camera/
mkdir -p $data_dir

rm $data_dir*

cd $data_dir


# From https://www.raspberrypi.com/documentation/accessories/camera.html#libcamera-vid

# echo '1 second video with h.264 encoding'
# time libcamera-vid -t 1000 -o test.h264
# echo
# echo

# echo '1 second video with mjpeg encoding'
# time libcamera-vid -t 1000 --codec mjpeg -o test.mjpeg
# echo
# echo


# echo '1 second video with timestamp - creates mkv'
# time libcamera-vid -o test.h264 --save-pts timestamps.txt && \
# mkvmerge -o test.mkv --timecodes 0:timestamps.txt test.h264
# echo
# echo


# echo '1 second video transformed to mp4'
# time libcamera-vid -t 1000 -o test.h264
# time MP4Box -add test.h264 pivideo1.mp4
# echo
# echo


# echo '10 second video transformed to mp4'
# time libcamera-vid -t 10000 -o test.h264
# time MP4Box -add test.h264 pivideo10.mp4
# echo
# echo


# echo '100 second video transformed to mp4'
# time libcamera-vid -t 100000 -o test.h264
# time MP4Box -add test.h264 pivideo100.mp4
# echo
# echo

# Test various compressions - no real benefit
# echo '1 second video transformed zipped'
# time libcamera-vid -t 1000 -o test.h264
# time zip test.h264.zip test.h264
# time gzip -c test.h264 > test.h264.gzip
# # time gzip -k test.h264
# echo 'zip better'
# time zip -9 test.h264_9.zip test.h264
# time gzip -c9 test.h264 > test.h264_9.gzip
# # time MP4Box -add test.h264 pivideo100.mp4
# echo
# echo


# echo '1 second video mp4 transformed zipped'
# time libcamera-vid -t 1000 -o test.h264
# time MP4Box -add test.h264 pivideo.mp4
# time zip pivideo.mp4.zip pivideo.mp4
# time gzip -c pivideo.mp4 > pivideo.mp4.gzip
# echo 'zip better'
# time zip -9 pivideo.mp4_9.zip pivideo.mp4
# time gzip -c9 pivideo.mp4 > pivideo.mp4_9.gzip
# echo
# echo








################## IMAGES ##################


function run_and_get_time()
{
    command="${@: -1}" # Last arg
    eval "$command"
}

# Good arguments:
#   --immediate [=arg(=1)] (=0)           Perform first capture immediately, with no preview phase
#   -e [ --encoding ] arg (=jpg)          Set the desired output encoding, either jpg, png, rgb, bmp or yuv420
#   -q [ --quality ] arg (=93)            Set the JPEG quality parameter
#   --denoise arg (=auto)                 Sets the Denoise operating mode: auto, off, cdn_off, cdn_fast, cdn_hq
#   --framerate arg (=30)                 Set the fixed framerate for preview and video modes
#   --roi arg (=0,0,0,0)                  Set region of interest (digital zoom) e.g. 0.25,0.25,0.5,0.5
#   -n [ --nopreview ] [=arg(=1)] (=0)    Do not show a preview window
# echo 'various image encoders'

time libcamera-still -t 10000 -o test%d.jpg --timelapse 100

# time libcamera-still -n -o test.jpg
# time libcamera-still \
#     -n \
#     --immediate 1 \
#     --denoise off \
#     --flush 1 \
#     -t 0 \
#     -e png \
#     -o test.png

# time libcamera-still \
#     --nopreview \
#     --immediate 1 \
#     --denoise off \
#     --flush 1 \
#     -t 0 \
#     -e png \
#     -o test2.png
# time libcamera-still -e bmp -o test.bmp
# time libcamera-still -e rgb -o test.data
# time libcamera-still -e yuv420 -o test.data
# echo
# echo

