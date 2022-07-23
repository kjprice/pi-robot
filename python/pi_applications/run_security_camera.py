# https://datasheets.raspberrypi.com/camera/picamera2-manual-draft.pdf

# Ideas:
# - stream to udp and use pre_callback - this way we can display video in browser and record video
# - Capture individual images and build a video based on these images
# - Test the speed of various ways to record video

#!/usr/bin/python3

print('just for testing -delete me')

from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

from ..modules.config import SERVER_NAMES
from ..modules.server_module.server_module import ServerModule
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput, FileOutput
class SecurityCamera(ServerModule):
    video_in_pipe = None
    video_out_pipe = None
    _arg_flags = None
    def __init__(self, arg_flags=None) -> None:
        self._arg_flags = arg_flags
        self.video_in_pipe, self.video_out_pipe = Pipe()

        server_name = SERVER_NAMES.SECURITY_CAMERA
        self.other_thread_functions = (
            self.init_python_server,
        )

        super().__init__(server_name, arg_flags)
    
    def init_python_server(self):
        print('starting python server')
        class CORSRequestHandler (SimpleHTTPRequestHandler):
            def end_headers (self):
                self.send_header('Access-Control-Allow-Origin', '*')
                SimpleHTTPRequestHandler.end_headers(self)

        # TODO: Store in config
        PYTHON_SERVER_PORT=8999
        # TODO: Move to correct folder (/data/security_videos/)
        test(CORSRequestHandler, HTTPServer, port=PYTHON_SERVER_PORT)
        print('completed python server')

    
    def socket_init(self):
        self.sio.emit('set_socket_room', 'security_camera')

    # https://datasheets.raspberrypi.com/camera/picamera2-manual-draft.pdf
    # Section 9.3 - multiple outputs
    def run_continuously(self):
        picam2 = Picamera2()
        video_config = picam2.video_configuration({"size": (640, 480)})
        picam2.configure(video_config)

        encoder = H264Encoder(bitrate=1000000, repeat=True, iperiod=15)
        stream_output = FfmpegOutput("-f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments -hls_allow_cache 0 data/security_videos/stream/stream.m3u8")
        file_output = FileOutput()
        encoder.output = [stream_output, file_output]

        picam2.start_encoder(encoder)
        picam2.start()


        i = 0
        while True:
            i = i + 1
            if self.abort_signal_received:
                self.send_output('abort_signal_received - returning')
                return

            start = time.time()

            file_path = "data/security_videos/stream/{}_test.h264".format(i)
            self.send_output('Sending to {}'.format(file_path))
            file_output.fileoutput = file_path
            file_output.start()
            self.sleep(5)
            file_output.stop()

            end = time.time()
            time_diff = end - start
            print(f'{time_diff} seconds passed')

            if self.abort_signal_received:
                picam2.stop()
                return

            self.send_output('Rerunning')



def start_camera_process(arg_flags=None):
    camera_head = SecurityCamera(arg_flags)
    camera_head.start_threads()

if __name__ == '__main__':
    start_camera_process()