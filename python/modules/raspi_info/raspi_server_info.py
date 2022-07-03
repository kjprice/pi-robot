from typing import List

from simplejson.errors import JSONDecodeError
import requests

from ..config import load_json_config


# TODO: add method for "toString" equivalent
class RaspiServerInfo:
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
        
        if not is_server_online:
            self.processes = []

        self.is_online = is_server_online
        return True
    
    def to_json(self):
        return {
            'hostname': self.hostname,
            'is_online': self.is_online,
            'processes': self.processes,
        }

def setup_server_info() -> List[RaspiServerInfo]:
    servers = []
    config = load_json_config()
    server_hostnames = config['serverHostnames']
    server_port = config['portsByProcess']['nodeServerStatus']
    for server_hostname in server_hostnames:
        poll_server = RaspiServerInfo(server_hostname, server_port)
        servers.append(poll_server)
    
    return servers