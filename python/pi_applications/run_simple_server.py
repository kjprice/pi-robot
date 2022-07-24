from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import os

from ..modules.config import SERVER_NAMES, get_port_by_process_name_from_config
from ..modules.server_module.server_module import ServerModule

PYTHON_SERVER_PORT = get_port_by_process_name_from_config('pythonHttpServer')

class SimpleServer(ServerModule):
    def __init__(self, arg_flags=None) -> None:

        server_name = SERVER_NAMES.PYTHON_SIMPLE_SERVER

        super().__init__(server_name, arg_flags)
    
    
    def socket_init(self):
        self.sio.emit('set_socket_room', 'python_simple_server')

    def run_continuously(self):
        while True:
          print('starting python server')

          # TODO: This is weird - document better or preferably upgrade python so we can set the directory in config
          os.chdir('data')
          class CORSRequestHandler (SimpleHTTPRequestHandler):
              def end_headers (self):
                  self.send_header('Access-Control-Allow-Origin', '*')
                  SimpleHTTPRequestHandler.end_headers(self)

          # TODO: Add timestampe to file output
          test(CORSRequestHandler, HTTPServer, port=PYTHON_SERVER_PORT)
          print('completed python server')

def start_simple_server(arg_flags=None):
    camera_head = SimpleServer(arg_flags)
    camera_head.start_threads()

if __name__ == '__main__':
    start_simple_server()