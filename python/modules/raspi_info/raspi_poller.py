import time

from ..config import SERVER_NAMES
from ..server_module.server_module import ServerModule
from .raspi_server_info import RaspiServerInfo, setup_server_info

DELAY_BETWEEN_REQUESTS = 5

# Continuously polls raspberry pis to get their status
class RaspiPoller(ServerModule):
    poll_servers = None
    def __init__(self, arg_flags):
        self.poll_servers = setup_server_info()

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

    def on_status_change(self, server: RaspiServerInfo) -> None:
        self.emit('raspi_status_changed', server.to_json())
    
    def on_active_process_change(self, server: RaspiServerInfo) -> None:
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

