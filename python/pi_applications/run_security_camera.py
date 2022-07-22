# https://datasheets.raspberrypi.com/camera/picamera2-manual-draft.pdf

# Ideas:
# - stream to udp and use pre_callback - this way we can display video in browser and record video
# - Capture individual images and build a video based on these images
# - Test the speed of various ways to record video

#!/usr/bin/python3

print('just for testing -delete me')

from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

from ..modules.camera_module import image_generator, camera_setup
from ..modules.config import get_servo_url, SERVER_NAMES, get_port_by_name_from_config
from ..modules.server_module.server_module import ServerModule
from ..modules.raspi_video.save_video_input import SaveVideoInput
from ..modules.raspi_video.stream_video_input import StreamVideoInput
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput, FileOutput

class SecurityCameraOutput(ServerModule):
    from_video_pipe = None
    stream_in_pipe = None
    stream_out_pipe = None
    save_in_pipe = None
    save_out_pipe = None
    def __init__(self, arg_flags, from_video_pipe: Connection) -> None:
        self.save_in_pipe, self.save_out_pipe = Pipe()
        self.stream_in_pipe, self.stream_out_pipe = Pipe()
        self.from_video_pipe = from_video_pipe

        server_name = SERVER_NAMES.SECURITY_CAMERA_OUTPUT
        self.other_thread_functions = (
            self.stream_video,
            self.save_video,
        )
        super().__init__(server_name, arg_flags)

    def socket_init(self):
        self.sio.emit('set_socket_room', 'security_camera_output')
    
    def stream_video(self):
        stream_video_input = StreamVideoInput(self.send_output)
        while True:
            while self.stream_out_pipe.poll():
                output = self.stream_out_pipe.recv()
                stream_video_input.write(output)
                self.send_output('stream_video {}'.format(output))
            self.sleep(2)

    def save_video(self):
        save_video_input = SaveVideoInput(self.send_output)
        while True:
            while self.save_out_pipe.poll():
                output = self.save_out_pipe.recv()
                save_video_input.write(output)
                self.send_output('save_video {}'.format(output))
            self.send_output('save_video sleep')
            self.sleep(4)

    def run_continuously(self):
        self.send_output('SecurityCameraOutput run_continuously')
        while True:
            while self.from_video_pipe.poll():
                output = self.from_video_pipe.recv()
                self.send_output('save_video {}'.format(output))
                self.stream_in_pipe.send(output)
                self.save_in_pipe.send(output)
            self.send_output('save_video sleep')
            self.sleep(4)

def start_camera_output_process(arg_flags, from_video_pipe: Connection):
    print('start_camera_output_process')
    start_camera_output = SecurityCameraOutput(arg_flags, from_video_pipe)
    start_camera_output.start_threads()

class SecurityCamera(ServerModule):
    video_in_pipe = None
    video_out_pipe = None
    _arg_flags = None
    def __init__(self, arg_flags=None) -> None:
        self._arg_flags = arg_flags
        self.video_in_pipe, self.video_out_pipe = Pipe()

        server_name = SERVER_NAMES.SECURITY_CAMERA
        self.other_thread_functions = (
            # self.init_output,
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

    
    def init_output(self):
        print('init_output')
        start_camera_output_process(self._arg_flags, self.video_out_pipe)

    def socket_init(self):
        self.sio.emit('set_socket_room', 'security_camera')

    def get_video(self):
        self.sleep(0.1)
        i = 0
        while True:
            i = i + 1
            self.video_in_pipe.send(i)
            self.send_output('get_video')
            self.sleep(1)

    # https://datasheets.raspberrypi.com/camera/picamera2-manual-draft.pdf
    # Section 9.3 - multiple outputs
    def run_continuously(self):
        picam2 = Picamera2()
        video_config = picam2.video_configuration({"size": (640, 480)})
        picam2.configure(video_config)

        encoder = H264Encoder(bitrate=1000000, repeat=True, iperiod=15)
        # encoder = H264Encoder(repeat=True, iperiod=15)
        # output1 = FfmpegOutput("-f mpegts udp://<ip-address>:12345")
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

            # output = [
                # FfmpegOutput("-f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments -hls_allow_cache 0 data/security_videos/stream/stream.m3u8"),
                # 'test_saved_video.h264'

            # ]

            start = time.time()

            # picam2.start_recording(encoder, output)
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
                # picam2.stop_recording()
                picam2.stop()
                return

            # self.send_output('Pausing')
            # self.sleep(15)
            self.send_output('Rerunning')



def start_camera_process(arg_flags=None):
    camera_head = SecurityCamera(arg_flags)
    camera_head.start_threads()

if __name__ == '__main__':
    start_camera_process()