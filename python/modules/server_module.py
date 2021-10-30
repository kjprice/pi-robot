import concurrent.futures as cf
import datetime
import os

import socketio

try:
    from modules.config import append_log_info, get_log_dir_by_server_name, write_log_info, SOCKET_IO_HOST_URI, SERVER_NAMES
except ModuleNotFoundError:
    from config import append_log_info, get_log_dir_by_server_name, write_log_info, SOCKET_IO_HOST_URI, SERVER_NAMES

def handle_default_server_response(response):
    text = response.text
    status_code = response.status_code
    if response.status_code != 200:
        raise Exception('Unkown status code "{}" with text "{}"'.format(status_code, text))
    if text != 'success':
        raise Exception('"success" not retrieved from server. Instead, received "{}"'.format(text))

def get_log_filename(server_name: SERVER_NAMES):
    log_base_name = server_name.value
    timestamp = str(datetime.datetime.now())
    return '{}_{}.txt'.format(log_base_name, timestamp)

class ServerModule:
    is_socket_connected = False
    server_name = None
    def __init__(self, server_name: SERVER_NAMES, env=None):
        if not server_name in SERVER_NAMES:
            raise AssertionError('Expected server name "{}" to be one of: {}'.format(server_name, SERVER_NAMES))
        self.server_name = server_name
        self.server_name_str = server_name.value
        if env is not None:
            os.environ = env
        
        self.init_log_info()
    def start_threads(self):
        with cf.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.connect_to_socket,),
                executor.submit(self.run_with_exception_catch,),
            ]
            cf.as_completed(futures)
    
    def init_log_info(self):
        self.log_dir = get_log_dir_by_server_name(self.server_name)
        self.log_filename = get_log_filename(self.server_name)
        self.init_log_file()

    def init_log_file(self):
        write_log_info(self.log_dir, self.log_filename, '')
    
    def write_log(self, text):
        append_log_info(self.log_dir, self.log_filename, text)
        

    # All functions in here will act as socket io message receivers - these are used
    def connect_to_socket(self):
        self.sio = sio = socketio.Client()

        @sio.event
        def connect():
            self.is_socket_connected = True
            print('connection client')
            self.socket_init()
            
        @sio.event
        def disconnect():
            self.is_socket_connected = False
            print('disconnected from server')

        self.other_socket_events()
        sio.connect(SOCKET_IO_HOST_URI)
        sio.wait()

    def other_socket_events(self):
        pass

    def socket_init(self):
        pass
    
    def emit(self, message, data=None):
        if not self.is_socket_connected:
            return False
        self.sio.emit(message, data)
        return True
    
    def send_output(self, output_text: str):
        data = {
            'message': output_text,
            'server_name': self.server_name_str
        }
        self.write_log(output_text)
        if not self.emit('send_output', data):
            print(output_text)

    def run_with_exception_catch(self):
        try:
            self.run_continuously()
        except Exception as e:
            message = '\n'.join((
                'Found exception while trying to run {}:'.format(self.server_name_str),
                str(e)
            ))
            self.send_output(message)
            print(message)
            raise(e)

    def run_continuously(self):
        raise NotImplementedError
    