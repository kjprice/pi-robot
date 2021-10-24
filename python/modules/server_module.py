import concurrent.futures as cf
import os

import socketio

try:
    from modules.config import SOCKET_IO_HOST_URI
except ModuleNotFoundError:
    from config import SOCKET_IO_HOST_URI

def handle_default_server_response(response):
    text = response.text
    status_code = response.status_code
    if response.status_code != 200:
        raise Exception('Unkown status code "{}" with text "{}"'.format(status_code, text))
    if text != 'success':
        raise Exception('"success" not retrieved from server. Instead, received "{}"'.format(text))

class ServerModule:
    is_socket_connected = False
    def __init__(self, server_name, env=None):
        self.server_name = server_name
        if env is not None:
            os.environ = env
    def start_threads(self):
        with cf.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.connect_to_socket,),
                executor.submit(self.run_with_exception_catch,),
            ]
            cf.as_completed(futures)

    # All functions in here will act as socket io message receivers - these are used
    def connect_to_socket(self):
        self.sio = sio = socketio.Client()

        @sio.event
        def connect():
            self.is_socket_connected = True
            print('connection client')
            
        @sio.event
        def disconnect():
            self.is_socket_connected = False
            print('disconnected from server')

        sio.connect(SOCKET_IO_HOST_URI)
        sio.wait()
    
    def emit(self, message, data=None):
        if not self.is_socket_connected:
            return False
        self.sio.emit(message, data)
        return True
    
    def send_output(self, output_text):
        if not self.emit('output_{}'.format(self.server_name), output_text):
            print(output_text)

    def run_with_exception_catch(self):
        try:
            self.run_continuously()
        except Exception as e:
            message = '\n'.join((
                'Found exception while trying to run {}:'.format(self.server_name),
                str(e)
            ))
            self.send_output(message)
            print(message)
            raise(e)

    def run_continuously(self):
        raise NotImplementedError
    