#!/usr/bin/python3
import argparse
import os
import requests
import time

import imagezmq

# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.camera_module import image_generator, camera_setup
from modules.config import get_servo_url, SERVER_NAMES
from modules.image_processor import Image_Processor
from modules.server_module import handle_default_server_response, ServerModule

# We do not need too many images - it is ok to throw away some
# TODO: Decide which images to throw away based on if they are more blurry than others
MAX_IMAGES_TO_PROCESS_PER_SECOND = 6
GET_IMAGE_ENDPOINT = '/getImage'
FOLDER_TO_SAVE_TO = 'images-captured'

# If false, we will use pub/sub; the two patterns behave completely differently https://github.com/jeffbass/imagezmq/blob/48614483298b782b37dffdddd6b75b9ae0ee525c/docs/req-vs-pub.rst
REQ_REP = True

parser = argparse.ArgumentParser()
parser.add_argument(
    '--is_test',
    action='store_true',
    help='Set to true if this is running locally, otherwise it will try to use PiCamera'
)

args = parser.parse_args()

def is_test():
    if 'IS_TEST' in os.environ:
        return True
    
    return args.is_test

def get_servo_url_path(path):
    servo_url = get_servo_url(is_test())
    url = '/'.join([servo_url, path])

    return url

def test_connection_with_servo_server():
    url = get_servo_url_path('testConnection')
    print('Testing connection with servo server on url "{}"'.format(url))
    response = requests.get(url)
    handle_default_server_response(response)
    print('Successfully connected with servo server')

def test_connection_with_image_processing_server(url):
    response = requests.get('{}/testConnection'.format(url))
    text = response.text
    status_code = response.status_code
    if status_code == 200 and text == 'success':
        return True
    return False

def get_image_sender():
    if REQ_REP:
        return imagezmq.ImageSender(connect_to='tcp://kj-macbook.lan:6666', REQ_REP=True)
    else:
        return imagezmq.ImageSender(connect_to='tcp://*:6666', REQ_REP=False)

class CameraHead(ServerModule):
    is_processing_server_online = None
    image_processor = None
    count_images_discarded = 0
    count_images_used = 0
    time_started = None
    last_image_sent_time = None
    seconds_between_images = 2

    def __init__(self, env=None, seconds_between_images=None) -> None:
        if seconds_between_images is not None:
            self.seconds_between_images = seconds_between_images
        self.image_processor = Image_Processor()
        self.is_processing_server_online = False
        self.time_started = time.time()
        self.time_needed_between_images = 1 / MAX_IMAGES_TO_PROCESS_PER_SECOND

        server_name = SERVER_NAMES.CAMERA_HEAD
        super().__init__(server_name=server_name, env=env)
    
    def other_socket_events(self):
        sio = self.sio

        @sio.event
        def confirm_image_processing_server_online():
            self.send_output('Confirmed image processing server is online')
            self.is_processing_server_online = True
        
        @sio.event
        def chnage_seconds_between_images(seconds_between_images):
            self.send_output('Setting new seconds_between_images: {}'.format(seconds_between_images))
            self.seconds_between_images = seconds_between_images
    
    def socket_init(self):
        self.sio.emit('set_socket_room', 'camera_head')
    
    def check_if_processing_server_online(self):
        if not self.is_processing_server_online:
            self.emit('is_processing_server_online')

    def should_throttle_image(self):
        if self.last_image_sent_time is not None:
            now = time.time()
            if now - self.last_image_sent_time < self.time_needed_between_images:
                return False
        self.last_image_sent_time = time.time()
        return True

    def run_continuously(self):
        camera_setup(is_test(), grayscale=True)

        time.sleep(1) # Give time for camera to warm up

        # if not self.is_processing_server_online and not IS_TEST:
        #     test_connection_with_servo_server()

        images_count = 0
        sender = get_image_sender()

        for img, time_passed_for_image in image_generator(is_test()):
            self.check_if_processing_server_online()
            time.sleep(self.seconds_between_images)
            time_start = time.time() - time_passed_for_image
            images_count += 1
            # TODO: Periodically check to make sure that server is still online (every 10 seconds)
            if self.is_processing_server_online:
                if self.should_throttle_image():
                    self.count_images_used += 1
                    # TODO: Decide whether to make greyscale before saving - compare time savings
                    sender.send_image(str(time.time()), img)
                else:
                    self.count_images_discarded += 1
                self.send_output('Found {} image(s) and dropped {} image(s)'.format(self.count_images_used, self.count_images_discarded))
            else:
                self.image_processor.process_message_immediately(img, time_passed_for_image, time_start)

def start_camera_process(env=None, seconds_between_images=None):
    camera_head = CameraHead(env, seconds_between_images=seconds_between_images)
    camera_head.start_threads()

if __name__ == '__main__':
    start_camera_process()