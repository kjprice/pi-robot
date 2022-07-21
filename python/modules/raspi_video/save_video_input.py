from .video_input import VideoInputAbstract

class SaveVideoInput(VideoInputAbstract):
    def write(self, data) -> None:
        self.send_output('write SaveVideoInput')
    def flush(self) -> None:
        pass
