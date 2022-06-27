import time
from typing import List

import requests

from ..config import SERVER_NAMES, load_json_config
from .server_module import ServerModule

# TODO: add method for "toString" equivalent
class PollServer:
    is_online = None
    hostname = None
    address = None
    def __init__(self, hostname: str, port: int) -> None:
        self.is_online = False
        self.hostname = hostname
        self.address = f'http://{hostname}:{port}'
    
    def run_ping(self):
        ping_url = f'{self.address}/ping'
        print(ping_url)
        is_server_online = False
        try:
            r = requests.get(ping_url)
            is_server_online = r.status_code == 200
        except requests.exceptions.ConnectionError:
            is_server_online = False
        
        return is_server_online

    def hasStatusChanged(self):
        is_server_online = self.run_ping()

        if self.is_online == is_server_online:
            return False

        self.is_online = is_server_online
        return True


def setup_servers() -> List[PollServer]:
    servers = []
    config = load_json_config()
    server_hostnames = config['serverHostnames']
    server_port = config['healthStatusPort']
    for server_hostname in server_hostnames:
        poll_server = PollServer(server_hostname, server_port)
        servers.append(poll_server)
    
    return servers


# Continuously polls raspberry pis to get their status
class RaspiPoller(ServerModule):
    poll_servers = None
    def __init__(self, arg_flags):
        self.poll_servers = setup_servers()

        server_name = SERVER_NAMES.RASPI_POLLER
        super().__init__(server_name, arg_flags)

    def socket_init(self):
        # TODO: Move to config
        self.sio.emit('set_socket_room', 'raspi_poller')
        # TODO: Initially send the status of the servers

    def other_socket_events(self):
        super().other_socket_events()

    def on_status_change(self, server: PollServer) -> None:
        data = {
            'hostname': server.hostname,
            'is_online': server.is_online
        }
        self.emit('raspi_status_changed', data)
    def run_continuously(self):
        while True:
            for server in self.poll_servers:
                if server.hasStatusChanged():
                    self.send_output('{} online changed to {}'.format(server.hostname, server.is_online))
                    self.on_status_change(server)
            time.sleep(10)

