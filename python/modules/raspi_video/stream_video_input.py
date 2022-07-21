from .video_input import VideoInputAbstract

class StreamVideoInput(VideoInputAbstract):
    def write(self, data) -> None:
        self.send_output('write StreamVideoInput')
    def flush(self) -> None:
        pass
