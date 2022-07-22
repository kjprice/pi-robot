from typing import Callable
from .video_input import VideoInputAbstract
from picamera2.outputs import FfmpegOutput

# TODO: Delete this


class StreamVideoInput(VideoInputAbstract):
    output = None
    def __init__(self, send_output: Callable) -> None:
        self.output = FfmpegOutput("-f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments -hls_allow_cache 0 stream.m3u8")
        super().__init__(send_output)
    def write(self, data) -> None:
        self.send_output('write StreamVideoInput')
        self.output.write(data)
    def flush(self) -> None:
        pass
