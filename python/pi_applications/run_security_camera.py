# https://datasheets.raspberrypi.com/camera/picamera2-manual-draft.pdf

# Ideas:
# - stream to udp and use pre_callback - this way we can display video in browser and record video
# - Capture individual images and build a video based on these images
# - Test the speed of various ways to record video

#!/usr/bin/python3

from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

from ..modules.camera_module import image_generator, camera_setup
from ..modules.config import get_servo_url, SERVER_NAMES, get_port_by_name_from_config
from ..modules.server_module.server_module import ServerModule


class SecurityCamera(ServerModule):
    in_pipe = None
    out_pipe = None
    def __init__(self, arg_flags=None) -> None:
        self.in_pipe, self.out_pipe = Pipe()
        server_name = SERVER_NAMES.SECURITY_CAMERA
        self.other_thread_functions = (
            # self.get_video,
            self.stream_video,
            self.save_video,
        )
        super().__init__(server_name, arg_flags)
    
    def socket_init(self):
        self.sio.emit('set_socket_room', 'security_camera')

    def get_video(self):
        self.sleep(0.1)
        i = 0
        while True:
            i = i + 1
            self.in_pipe.send('save_video_pipe {}'.format(i))
            self.send_output('get_video')
            self.sleep(1)
        pass
    # Needs "write" and "flush" methods
    # TODO: Create a Process for this
    def stream_video(self):
        self.sleep(0.1)
        while True:
            self.send_output('stream_video')
            self.sleep(1)
        pass
    # TODO: Create a Process for this
    def save_video(self):
        while True:
            while self.out_pipe.poll():
                output = self.out_pipe.recv()
                self.send_output('output', output)
            self.sleep(4)

    def run_continuously(self):
        while True:
            if self.abort_signal_received:
                self.send_output('abort_signal_received - returning')
                return
            self.get_video()

def start_camera_process(arg_flags=None):
    camera_head = SecurityCamera(arg_flags)
    camera_head.start_threads()

if __name__ == '__main__':
    start_camera_process()