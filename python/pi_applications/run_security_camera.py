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
    stream_in_pipe = None
    stream_out_pipe = None
    save_in_pipe = None
    save_out_pipe = None
    def __init__(self, arg_flags=None) -> None:
        self.save_in_pipe, self.save_out_pipe = Pipe()
        # self.stream_in_pipe, self.stream_out_pipe = Pipe()
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
            # self.stream_in_pipe.send(i)
            self.save_in_pipe.send(i)
            self.send_output('get_video')
            self.sleep(1)
        pass
    # Needs "write" and "flush" methods
    # TODO: Create a Process for this
    def stream_video(self):
        return
        while True:
            while self.stream_out_pipe.poll():
                output = self.stream_out_pipe.recv()
                self.send_output('stream_video {}'.format(output))
            self.sleep(2)
    # TODO: Create a Process for this
    def save_video(self):
        print('save_video')
        while True:
            while self.save_in_pipe.poll():
                output = self.save_in_pipe.recv()
                self.send_output('save_video {}'.format(output))
            print('save_video sleep')
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