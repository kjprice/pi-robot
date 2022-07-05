# TODO:
# - Give an option to run all the things - including:
#  - ssh or local camera head
#  - image processing-server
#  - servo server

# TODO: Move to config
BROWSERS_ROOM_NAME = 'browsers'

import os
import time
from typing import List

import eventlet
import socketio

from ..modules.config import SERVER_NAMES, SOCKET_IO_SERVER_PORT, SOCKET_ROOMS, STATIC_DIR, load_json_config, get_local_ip, SOCKET_IO_HOST_URI, SOCKET_IO_HOST_URI_LOCAL
from ..modules.workers.job_process.job_process import JobProcess
from ..modules.workers.job_process.ssh_process import SSH_Process, kill_process_by_name
from ..modules.raspi_info.raspi_poller import RaspiPoller

from ..pi_applications.run_image_processing_server import run_image_processing_server
from ..pi_applications.run_camera_head_server import start_camera_process

from .misc.web_app_helper_text import print_startup_details
class WebApp():
  jobs_running_by_fn_name = None
  raspi_info_by_hostname = None
  def __init__(self) -> None:
    self.jobs_running_by_fn_name = {}
    self.raspi_info_by_hostname = {}

    self.create_raspi_poller_job()
    print_startup_details()
    self.start_socket_server()
  
  def stop_job_if_exists_by_fn_name(self, fn_name):
    if fn_name in self.jobs_running_by_fn_name:
      self.jobs_running_by_fn_name[fn_name].terminate()
      del self.jobs_running_by_fn_name[fn_name]

  def stop_all_server_processes(self):
    fn_names = list(self.jobs_running_by_fn_name.keys())
    for fn_name in fn_names:
      self.stop_job_if_exists_by_fn_name(fn_name)
    
    print('Shut off {} servers'.format(len(fn_names)))

  def add_default_arg_flags(self, provided_flags: str = ""):
    socket_server_uri_flag = f'--socket_server_uri={SOCKET_IO_HOST_URI}'
    socket_server_uri_local_flag = f'--socket_server_local_uri={SOCKET_IO_HOST_URI_LOCAL}'
    all_flags = [
      socket_server_uri_flag,
      socket_server_uri_local_flag,
    ]

    if provided_flags:
      all_flags.append(provided_flags)


    return ' '.join(all_flags)

  def create_job(self, fn_name, fn_reference, arg_flags=""):
    self.stop_job_if_exists_by_fn_name(fn_name)

    arg_flags = self.add_default_arg_flags(arg_flags)
    job = JobProcess(fn_reference, arg_flags)

    self.jobs_running_by_fn_name[fn_name] = job

  def get_fn_for_ssh_job(self, hostname: str, script_str: str):
    return '{}|{}'.format(hostname, script_str)

  def create_job_ssh(self, hostname: str, process_name: str, flags: str = ''):
    fn_name = self.get_fn_for_ssh_job(hostname, process_name)
    self.stop_job_if_exists_by_fn_name(fn_name)
    flags = self.add_default_arg_flags(flags)
    job = SSH_Process(hostname, process_name, flags)
    self.jobs_running_by_fn_name[fn_name] = job

  def start_process_ssh(self, hostname: str, process_name: str, flags: str = ''):
    flags = self.add_default_arg_flags(flags)
    SSH_Process(hostname, process_name, flags)

  def stop_process_ssh(self, hostname: str, process_name: str, flags: str = ''):
    flags = self.add_default_arg_flags(flags)
    kill_process_by_name(hostname, process_name)

  def create_image_processing_server_job(self, classification_model: str):
    arg_flags = ''
    if classification_model is not None:
      arg_flags = '--classification_model {}'.format(classification_model)
    server_name = SERVER_NAMES.IMAGE_PROCESSING.value
    self.create_job(server_name, run_image_processing_server, arg_flags)

  def start_poller(self, arg_flags):
    poller = RaspiPoller(arg_flags)
    poller.start_threads()

  def get_first_online_raspi_hostname(self):
    for raspi_info in self.raspi_info_by_hostname.values():
      if raspi_info['is_online']:
        return raspi_info['hostname']
    return None

  def create_camera_head_server_job(self, use_remote_servers: bool, seconds_between_images: int, classification_model: str):
    self.get_first_online_raspi_hostname()
    server_name = SERVER_NAMES.CAMERA_HEAD.value
    arg_flags = '--delay {}'.format(seconds_between_images)
    arg_flags += ' --classification_model {}'.format(classification_model)
    raspi_hostname = self.get_first_online_raspi_hostname()

    if use_remote_servers and raspi_hostname is not None:
      print('Attempting to run camera head job on {}'.format(raspi_hostname))
      # TODO: Move hostname to config or let user pick which raspi to connect to
      self.create_job_ssh('pi@{}'.format(raspi_hostname), 'robotCameraHead', arg_flags)
    else:
      arg_flags += ' --is_test'
      self.create_job(server_name, start_camera_process, arg_flags)

  def create_servo_server_job(self):
      self.create_job_ssh('pi3misc', 'run_servo_server')

  def create_raspi_poller_job(self):
    JobProcess(self.start_poller, self.add_default_arg_flags())
  
  def set_raspi_info(self, raspi_servers_info: List[dict]):
    for raspi_server_info in raspi_servers_info:
      self.raspi_info_by_hostname[raspi_server_info['hostname']] = raspi_server_info

  def start_socket_server(self):
    sio = self.sio = socketio.Server(cors_allowed_origins='*')
    app = socketio.WSGIApp(sio, static_files={
        '/': os.path.join(STATIC_DIR, 'index.html'),
        '/static': os.path.join(STATIC_DIR, 'static')
    })

    # From all clients
    @sio.event
    def connect(sid, environ):
      print('connect ', sid)

    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)

    @sio.event
    def set_socket_room(sid, room_name):
      if not room_name in SOCKET_ROOMS:
        raise AssertionError('Expected room_name "{}" to be one of: {}'.format(room_name, SOCKET_ROOMS))

      sio.enter_room(sid, room_name)
      print('setting client "{}" to room "{}"'.format(sid, room_name))

      # output='test'
      # print('send_output', output)
      # data = {
      #   'message': output,
      #   # TODO: Update this
      #   'server_name': 'pi3'

      # }
      # print('self.sio', self.sio)
      # self.sio.emit('send_output', data, room=BROWSERS_ROOM_NAME)
      # print('self.sio sent')


    # From all backend clients (not browser)
    # TODO: Use this
    @sio.event
    def send_output(sid, data):
      print('send_output', data)
      sio.emit('send_output', data, room=BROWSERS_ROOM_NAME)

    # From raspi poller
    @sio.event
    def raspi_status_changed(sid, server):
      self.set_raspi_info([server])
      sio.emit('raspi_status_changed', server, room=BROWSERS_ROOM_NAME)

    @sio.event
    def raspi_active_processes_changed(sid, server):
      self.set_raspi_info([server])
      print('raspi_active_processes_changed')
      sio.emit('raspi_status_changed', server, room=BROWSERS_ROOM_NAME)

    # From browser
    @sio.event
    def load_all_servers(sid, data):
      seconds_between_images = data['delay']
      use_remote_servers = data['remote']
      classification_model = data['classification_model']
      step = 1
      sio.emit('all_servers_loading_status', { 'step': step, 'details': 'create image processing server job' }, sid)
      step += 1
      self.create_image_processing_server_job(classification_model=classification_model)
      sio.emit('all_servers_loading_status', { 'step': step, 'details': 'create camera head server job' }, sid)
      step += 1
      self.create_camera_head_server_job(use_remote_servers=use_remote_servers, seconds_between_images=seconds_between_images, classification_model=classification_model)
      if use_remote_servers:
        self.create_servo_server_job()
        sio.emit('all_servers_loading_status', { 'step': step, 'details': 'create servo server job' }, sid)
        step += 1

      sio.emit('all_servers_loading_status', { 'step': step, 'details': 'complete' }, sid)
    
    @sio.event
    def start_process(sid, data):
      hostname = data['hostname']
      process_name = data['processName']
      self.start_process_ssh(hostname, process_name)

    @sio.event
    def stop_process(sid, data):
      hostname = data['hostname']
      process_name = data['processName']
      self.stop_process_ssh(hostname, process_name)

    @sio.event
    def stop_all_servers(sid):
      sio.emit('shutdown_now', room='image_processing_server')
      sio.emit('shutdown_now', room='camera_head')
      # TODO: This should be put on a different thread
      time.sleep(1)
      self.stop_all_server_processes()
      sio.emit('all_servers_stopped_status', to=sid)

    @sio.event
    def get_server_statuses(sid):
      jobs_running = self.jobs_running_by_fn_name.keys()
      config = load_json_config()
      sio.emit('browser_init_status', {'jobs_running': list(jobs_running), 'config': config}, to=sid)

      sio.emit('request_raspi_statuses', room='raspi_poller')
      @sio.event
      def all_raspi_statuses(_, servers):
        self.set_raspi_info(servers)
        sio.emit('all_raspi_statuses', servers, to=sid)


    @sio.event
    def processed_image_finished(sid, message):
      sio.emit('processed_image_finished', message, room=BROWSERS_ROOM_NAME)

    @sio.event
    def is_processing_server_online(sid):
      sio.emit('is_processing_server_online', room='image_processing_server')

    @sio.event
    def delay_change(sid, _delay_change):
      sio.emit('change_seconds_between_images', _delay_change, room='camera_head')

    @sio.event
    def change_classification_model(sid, classification_model):
      print('classification_model from browser', classification_model)
      sio.emit('set_new_classification_model', classification_model)

    @sio.event
    def confirm_image_processing_server_online(sid):
      sio.emit('confirm_image_processing_server_online', room='camera_head')

    eventlet.wsgi.server(eventlet.listen((get_local_ip(), SOCKET_IO_SERVER_PORT)), app)

if __name__ == '__main__':
  WebApp()
  