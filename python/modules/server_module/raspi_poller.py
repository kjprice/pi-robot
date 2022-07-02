import time
from typing import List

from simplejson.errors import JSONDecodeError
import requests

from ..config import SERVER_NAMES, load_json_config
from .server_module import ServerModule

DELAY_BETWEEN_REQUESTS = 5

# TODO: add method for "toString" equivalent
class PollServer:
    is_online = None
    hostname = None
    address = None
    processes = None
    def __init__(self, hostname: str, port: int) -> None:
        self.is_online = False
        self.hostname = hostname
        self.processes = []
        self.address = f'http://{hostname}:{port}'
    
    def run_ping(self):
        ping_url = f'{self.address}/ping'
        is_server_online = False
        SECONDS_BEFORE_TIMEOUT = 2
        try:
            r = requests.get(ping_url, timeout=SECONDS_BEFORE_TIMEOUT)
            is_server_online = r.status_code == 200
        except requests.exceptions.ConnectionError:
            is_server_online = False
        
        return is_server_online

    def fetch_active_processes(self):
        url = f'{self.address}/processes'
        r = requests.get(url)
        try:
            return r.json()
        except JSONDecodeError:
            return []
    
    def has_active_processes_changed(self):
        processes = self.fetch_active_processes()

        if self.processes == processes:
            return False
        
        self.processes = processes
        return True

    def hasStatusChanged(self):
        is_server_online = self.run_ping()

        if self.is_online == is_server_online:
            return False

        self.is_online = is_server_online
        return True
    
    def to_json(self):
        return {
            'hostname': self.hostname,
            'is_online': self.is_online,
            'processes': self.processes,
        }

def setup_servers() -> List[PollServer]:
    servers = []
    config = load_json_config()
    server_hostnames = config['serverHostnames']
    server_port = config['portsByProcess']['nodeServerStatus']
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
        sio = self.sio

        @sio.event
        def request_raspi_statuses():
            self.send_output('request_raspi_statuses')
            self.send_all_raspi_statuses()
    
    def send_all_raspi_statuses(self):
        servers = [server.to_json() for server in self.poll_servers]
        self.emit('all_raspi_statuses', servers)

    def on_status_change(self, server: PollServer) -> None:
        self.emit('raspi_status_changed', server.to_json())
    
    def on_active_process_change(self, server: PollServer) -> None:
        self.emit('raspi_active_processes_changed', server.to_json())

    def run_continuously(self):
        while True:
            for server in self.poll_servers:
                if server.hasStatusChanged():
                    self.send_output('{} online changed to {}'.format(server.hostname, server.is_online))
                    self.on_status_change(server)
            for server in self.poll_servers:
                if server.is_online and server.has_active_processes_changed():
                    self.on_active_process_change(server)

            time.sleep(DELAY_BETWEEN_REQUESTS)

