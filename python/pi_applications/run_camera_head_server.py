#!/usr/bin/python3
import os
import requests
import time

import imagezmq

from ..modules.camera_module import image_generator, camera_setup
from ..modules.config import get_servo_url, SERVER_NAMES, get_port_by_name_from_config
from ..modules.server_module.server_classification_module import Server_Classification_Module

# We do not need too many images - it is ok to throw away some
# TODO: Decide which images to throw away based on if they are more blurry than others
MAX_IMAGES_TO_PROCESS_PER_SECOND = 6
GET_IMAGE_ENDPOINT = '/getImage'
FOLDER_TO_SAVE_TO = 'images-captured'

# If false, we will use pub/sub; the two patterns behave completely differently https://github.com/jeffbass/imagezmq/blob/48614483298b782b37dffdddd6b75b9ae0ee525c/docs/req-vs-pub.rst
REQ_REP = True

WEB_SERVER_PORT = get_port_by_name_from_config('webServerPort')
IMAGE_HUB_PORT = get_port_by_name_from_config('imageHubPort')

def get_servo_url_path(path: str, is_test: bool):
    servo_url = get_servo_url(is_test)
    url = '/'.join([servo_url, path])

    return url

def test_connection_with_image_processing_server(url):
    response = requests.get('{}/testConnection'.format(url))
    text = response.text
    status_code = response.status_code
    if status_code == 200 and text == 'success':
        return True
    return False

def get_image_sender(uri):
    if REQ_REP:
        # TODO: Add port to config.json
        return imagezmq.ImageSender(connect_to=uri, REQ_REP=True)
    else:
        return imagezmq.ImageSender(connect_to=uri, REQ_REP=False)

class CameraHead(Server_Classification_Module):
    is_processing_server_online = None
    image_processor = None
    count_images_discarded = 0
    count_images_used = 0
    time_started = None
    last_image_sent_time = None
    sender = None
    _seconds_between_images = None

    def __init__(self, arg_flags=None) -> None:
        self.is_processing_server_online = False
        self.time_started = time.time()
        self.time_needed_between_images = 1 / MAX_IMAGES_TO_PROCESS_PER_SECOND

        server_name = SERVER_NAMES.CAMERA_HEAD
        super().__init__(server_name, arg_flags)
    
    def other_args(self):
        super().other_args()
        self.parser.add_argument(
            '--delay',
            type=int,
            default=2
        )

    def other_socket_events(self):
        super().other_socket_events()
        sio = self.sio

        @sio.event
        def confirm_image_processing_server_online():
            self.send_output('Confirmed image processing server is online')
            socket_uri=self.socket_server_uri
            self.send_output('Connecting to sender at {}'.format(socket_uri))
            # TODO: Pass in actual uri so we do not have to convert
            uri=socket_uri.replace('http', 'tcp').replace(str(WEB_SERVER_PORT), str(IMAGE_HUB_PORT))
            self.send_output('Converted uri to {}'.format(uri))
            self.sender = get_image_sender(uri)
            self.is_processing_server_online = True
        
        @sio.event
        def change_seconds_between_images(seconds_between_images):
            self.send_output('Setting new seconds_between_images: {}'.format(seconds_between_images))
            self._seconds_between_images = seconds_between_images
        self.send_output('other_socket_events 2')
    
    def socket_init(self):
        self.sio.emit('set_socket_room', 'camera_head')
    
    def check_if_processing_server_online(self):
        self.send_output('self.is_processing_server_online', self.is_processing_server_online)
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
        camera_setup(self.is_test, grayscale=True)

        self.sleep(1) # Give time for camera to warm up

        # if not self.is_processing_server_online and not IS_TEST:
        #     test_connection_with_servo_server(self.is_test)

        images_count = 0

        for img, time_passed_for_image in image_generator(self.is_test, grayscale=False):
            self.check_if_processing_server_online()
            self.sleep(self.seconds_between_images)
            if self.abort_signal_received:
                self.send_output('aborting')
                return
            time_start = time.time() - time_passed_for_image
            images_count += 1
            # TODO: Periodically check to make sure that server is still online (every 10 seconds)
            if self.is_processing_server_online:
                if self.should_throttle_image():
                    self.count_images_used += 1
                    # TODO: Decide whether to make greyscale before saving - compare time savings
                    self.sender.send_image(str(time.time()), img)
                else:
                    self.count_images_discarded += 1
                self.send_output('Found {} image(s) and dropped {} image(s)'.format(self.count_images_used, self.count_images_discarded))
            else:
                self.image_processor.process_message_immediately(img, time_passed_for_image, time_start)

    @property
    def seconds_between_images(self):
        if self._seconds_between_images is not None:
            return self._seconds_between_images
        
        return self.get_args().delay

    @seconds_between_images.setter
    def seconds_between_images(self, value):
        self._seconds_between_images = value

def start_camera_process(arg_flags=None):
    camera_head = CameraHead(arg_flags)
    camera_head.start_threads()

if __name__ == '__main__':
    start_camera_process()