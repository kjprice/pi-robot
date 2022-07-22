from typing import Callable
# TODO: Delete this

class VideoInputAbstract:
    send_output = None
    def __init__(self, send_output: Callable) -> None:
        self.send_output = send_output
    def write(self, data) -> None:
        pass
    def flush(self) -> None:
        pass
