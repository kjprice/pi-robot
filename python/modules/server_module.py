import argparse
import concurrent.futures as cf
import datetime
import time

import socketio

try:
    from modules.config import append_log_info, get_log_dir_by_server_name, write_log_info, SOCKET_IO_HOST_URI, SERVER_NAMES
except ModuleNotFoundError:
    from config import append_log_info, get_log_dir_by_server_name, write_log_info, SOCKET_IO_HOST_URI, SERVER_NAMES

TIME_IN_SECONDS_BETWEEN_CHECKING_STATUS = 0.001

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

def output_text_from_args(*args):
    output_text = []
    for _arg in args:
        output_text.append(str(_arg))
    return ' '.join(output_text)

class ServerModule:
    is_socket_connected = False
    server_name = None
    abort_signal_received = False
    other_thread_functions = []
    flags = None
    def __init__(self, server_name: SERVER_NAMES, arg_flags):
        if not server_name in SERVER_NAMES:
            raise AssertionError('Expected server name "{}" to be one of: {}'.format(server_name, SERVER_NAMES))
        self.server_name = server_name
        self.server_name_str = server_name.value
        
        self.init_log_info()
        self.setup_args()
        self.set_flags(arg_flags)

    def start_threads(self):
        with cf.ThreadPoolExecutor() as executor:
            thread_functions = [self.connect_to_socket, self.run_with_exception_catch, *self.other_thread_functions]
            futures = [
                executor.submit(fn) for fn in thread_functions
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
            self.send_output('connection client')
            self.socket_init()
            
        @sio.event
        def disconnect():
            self.is_socket_connected = False
            self.send_output('disconnected from server')
        
        @sio.event
        def shutdown_now():
            self.send_output('Abort signal received')
            self.abort_signal_received = True

        self.other_socket_events()
        sio.connect(SOCKET_IO_HOST_URI)
        sio.wait()
    
    # Run time.sleep() while continuously checking to make sure we shouldn't abort
    def sleep(self, delay: float):
        start = time.time()
        while True:
            end = time.time()
            if self.abort_signal_received:
                return
            if delay <= end - start:
                return
            time.sleep(TIME_IN_SECONDS_BETWEEN_CHECKING_STATUS)

    def other_socket_events(self):
        pass

    def socket_init(self):
        pass

    def set_flags(self, flags):
        if flags is None:
            return
        
        self.flags = flags.split(' ')

    def setup_args(self):
        self.parser = parser = argparse.ArgumentParser()
        parser.add_argument(
            '--is_test',
            action='store_true',
            help='Set to true if this is running locally, otherwise it will try to use PiCamera'
        )

        self.other_args()
    
    def other_args(self):
        pass

    def get_args(self):
        if self.flags is not None:
            return self.parser.parse_args(self.flags)
        return self.parser.parse_args()
    
    @property
    def is_test(self):
        return self.get_args().is_test
    
    def emit(self, message, data=None):
        if not self.is_socket_connected:
            return False
        self.sio.emit(message, data)
        return True
    
    def send_output(self, *args):
        output_text = output_text_from_args(*args)
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
    