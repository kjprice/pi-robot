#!/usr/bin/python3

import concurrent.futures as cf
import os
import time

import imagezmq

from ..modules.config import SERVER_NAMES, get_port_by_name_from_config
from ..modules.image_module import get_file_path_for_save
from ..modules.server_module.server_classification_module import Server_Classification_Module
from ..modules.workers.image_stream_worker import get_perpetual_list_of_images_from_worker

IS_TEST = 'IS_TEST' in os.environ

IMAGE_HUB_PORT = get_port_by_name_from_config('imageHubPort')

# If false, we will use pub/sub; the two patterns behave completely differently https://github.com/jeffbass/imagezmq/blob/48614483298b782b37dffdddd6b75b9ae0ee525c/docs/req-vs-pub.rst
REQ_REP = True
# Setting this assumes that camera head is running locally
LOCAL_PUB_SUB = (not REQ_REP) and 'LOCAL_PUB_SUB' in os.environ

CACHE_FILE_NAME = 'camera_server_info.json'

# Global variables
camera_hostname = None
camera_image_endpoint = None
async_process = None

ALLOWED_HOSTNAMES = [
  'pirobot',
  'kj-macbook.lan', # KJ Macbook
]

def get_image_hub_uri_for_pub_sub():
    # TODO: Update this from config
    hostname = 'kj-macbook.lan' if LOCAL_PUB_SUB else 'pirobot'
    return 'tcp://{}:{}'.format(hostname, IMAGE_HUB_PORT)

perpetual_images = None

def get_image_hub():
    print('REQ_REP', REQ_REP)
    if REQ_REP:
        # This listens to this machine's port
        uri = f'tcp://*:{IMAGE_HUB_PORT}'
        return imagezmq.ImageHub(open_port=uri, REQ_REP=True)

# TODO: Move to its own class
last_image_time = None
# When we use PUB/SUB, the process is async and the images stack, we want to clear the old images
def get_image_for_pub_sub_from_image_hub(image_hub):
    global perpetual_images, last_image_time

    if perpetual_images is None:
        perpetual_images = get_perpetual_list_of_images_from_worker(get_image_hub_uri_for_pub_sub())
    while len(perpetual_images) == 0:
        print('Waiting for images to replenish')
        time.sleep(0.5)
    
    # TODO: We want diffs of latest_time, camera_timestamp, and current time (a new var) as stats
    latest_image, latest_time, camera_timestamp = perpetual_images[0]
    if latest_time == last_image_time:
        raise Exception('It looks like the same image was used twice')
    return ('', latest_image)

def get_image_from_image_hub(image_hub):
    if REQ_REP:
        return image_hub.recv_image()
    return get_image_for_pub_sub_from_image_hub(image_hub)

# This runs two concurrent threads: one to handle incoming socket communication and the other to handle processing images
class ImageProcessingServer(Server_Classification_Module):
    def __init__(self, arg_flags):
        server_name = SERVER_NAMES.IMAGE_PROCESSING
        super().__init__(server_name, arg_flags)

    def socket_init(self):
        self.sio.emit('set_socket_room', 'image_processing_server')

    def other_socket_events(self):
        super().other_socket_events()
        sio = self.sio

        @sio.event
        def is_processing_server_online():
            self.send_output('Confirming image processing server is online')
            self.emit('confirm_image_processing_server_online')
            self.is_processing_server_online = True


    def run_continuously(self):
        images_count = 0
        image_hub = get_image_hub()
        while True:
            time_start = time.time()
            time_to_pull = None
            rpi_name, image = get_image_from_image_hub(image_hub)
            time_end = time.time()
            time_to_pull = time_end - time_start
            images_count += 1

            if image is not None:
                self.image_processor.process_message_immediately(image, time_to_pull, time_start)
                # TODO: This is inneficiant - maybe even just send the path of the image and let the browser handle the image path
                # TODO: Pull this from memory
                with open(get_file_path_for_save('test-objects-detected-image.jpg'), 'rb') as f:
                    self.emit('processed_image_finished', f.read())
            
            if REQ_REP:
                image_hub.send_reply(b'OK')

def run_image_processing_server(arg_flags=None):
    image_processing_server = ImageProcessingServer(arg_flags)
    image_processing_server.start_threads()

if __name__ == '__main__':
    run_image_processing_server()
