# TODO:
# - Give an option to run all the things - including:
#  - ssh or local camera head
#  - image processing-server
#  - servo server

import os
import time

import eventlet
import socketio

from .modules.config import get_hostname, SERVER_NAMES, SOCKET_IO_SERVER_PORT, SOCKET_ROOMS, STATIC_DIR, load_json_config
from .modules.workers.job_process.job_process import JobProcess
from .modules.workers.job_process.ssh_process import SSH_Process
from .modules.server_module.raspi_poller import RaspiPoller

# from .pi_applications
from .pi_applications.run_image_processing_server import run_image_processing_server
from .pi_applications.run_camera_head_server import start_camera_process

jobs_running_by_fn_name = {}

def stop_job_if_exists_by_fn_name(fn_name):
  if fn_name in jobs_running_by_fn_name:
    jobs_running_by_fn_name[fn_name].terminate()
    del jobs_running_by_fn_name[fn_name]

def stop_all_server_processes():
  fn_names = list(jobs_running_by_fn_name.keys())
  for fn_name in fn_names:
    stop_job_if_exists_by_fn_name(fn_name)
  
  print('Shut off {} servers'.format(len(fn_names)))

def create_job(fn_name, fn_reference, arg_flags=None):
  stop_job_if_exists_by_fn_name(fn_name)

  job = JobProcess(fn_reference, arg_flags)

  jobs_running_by_fn_name[fn_name] = job

def get_fn_for_ssh_job(hostname: str, script_str: str):
  return '{}|{}'.format(hostname, script_str)

def create_job_ssh(hostname: str, process_name: str, flags: str = ''):
  fn_name = get_fn_for_ssh_job(hostname, process_name)
  stop_job_if_exists_by_fn_name(fn_name)
  job = SSH_Process(hostname, process_name, flags)
  jobs_running_by_fn_name[fn_name] = job

def create_image_processing_server_job(classification_model: str):
  arg_flags = ''
  if classification_model is not None:
    arg_flags = '--classification_model {}'.format(classification_model)
  server_name = SERVER_NAMES.IMAGE_PROCESSING.value
  create_job(server_name, run_image_processing_server, arg_flags)

def start_poller(arg_flags):
  poller = RaspiPoller(arg_flags)
  poller.start_threads()

def create_raspi_poller_job():
 JobProcess(start_poller, '')

def create_camera_head_server_job(use_remote_servers: bool, seconds_between_images: int, classification_model: str):
  server_name = SERVER_NAMES.CAMERA_HEAD.value
  arg_flags = '--delay {}'.format(seconds_between_images)
  arg_flags += ' --classification_model {}'.format(classification_model)
  if use_remote_servers:
    # TODO: Move to config
    create_job_ssh('pirobot', 'run_camera_head_server', arg_flags)
  else:
    arg_flags += ' --is_test'
    create_job(server_name, start_camera_process, arg_flags)

def create_servo_server_job():
    create_job_ssh('pi3misc', 'run_servo_server')

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': os.path.join(STATIC_DIR, 'index.html'),
    '/static': os.path.join(STATIC_DIR, 'static')
})

def create_homepage_url():
  return '\n'.join([
    '# Server URL',
    'http://{}:{}/'.format(get_local_ip(), SOCKET_IO_SERVER_PORT)
  ])

def create_wsl_forward_helper_text():
  port=SOCKET_IO_SERVER_PORT
  wsl_ip=get_local_ip()
  return '\n'.join([
    '# Port Forwarding (WSL)',
    'Follow the instructions on https://github.com/kjprice/pi-robot#server-running-on-wsl with the following information:',
    f'The IP for WSL is: {wsl_ip}',
    f'The port for WSL and Windows is: {SOCKET_IO_SERVER_PORT}',
  ])

print()
print('**********')
print()
print(create_homepage_url())
print()
print(create_wsl_forward_helper_text())
print()
print('**********')
print()

@sio.event
def connect(sid, environ):
  print('connect ', sid)

# TODO: Move to config
BROWSERS_ROOM_NAME = 'browsers'

@sio.event
def raspi_status_changed(sid, server):
  sio.emit('raspi_status_changed', server, room=BROWSERS_ROOM_NAME)


@sio.event
def set_socket_room(sid, room_name):
  if not room_name in SOCKET_ROOMS:
    raise AssertionError('Expected room_name "{}" to be one of: {}'.format(room_name, SOCKET_ROOMS))

  sio.enter_room(sid, room_name)
  print('setting client "{}" to room "{}"'.format(sid, room_name))

@sio.event
def load_all_servers(sid, data):
  seconds_between_images = data['delay']
  use_remote_servers = data['remote']
  classification_model = data['classification_model']
  step = 1
  sio.emit('all_servers_loading_status', { 'step': step, 'details': 'create image processing server job' }, sid)
  step += 1
  create_image_processing_server_job(classification_model=classification_model)
  sio.emit('all_servers_loading_status', { 'step': step, 'details': 'create camera head server job' }, sid)
  step += 1
  create_camera_head_server_job(use_remote_servers=use_remote_servers, seconds_between_images=seconds_between_images, classification_model=classification_model)
  if use_remote_servers:
    create_servo_server_job()
    sio.emit('all_servers_loading_status', { 'step': step, 'details': 'create servo server job' }, sid)
    step += 1

  sio.emit('all_servers_loading_status', { 'step': step, 'details': 'complete' }, sid)

@sio.event
def stop_all_servers(sid):
  sio.emit('shutdown_now', room='image_processing_server')
  sio.emit('shutdown_now', room='camera_head')
  # TODO: This should be put on a different thread
  time.sleep(1)
  stop_all_server_processes()
  sio.emit('all_servers_stopped_status', to=sid)

@sio.event
def get_server_statuses(sid):
  jobs_running = jobs_running_by_fn_name.keys()
  config = load_json_config()
  sio.emit('browser_init_status', {'jobs_running': list(jobs_running), 'config': config}, to=sid)

  sio.emit('request_raspi_statuses', room='raspi_poller')
  @sio.event
  def all_raspi_statuses(_, servers):
    sio.emit('all_raspi_statuses', servers, to=sid)


@sio.event
def processed_image_finished(sid, message):
  sio.emit('processed_image_finished', message, room=BROWSERS_ROOM_NAME)

@sio.event
def send_output(sid, data):
  sio.emit('send_output', data, room=BROWSERS_ROOM_NAME)

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

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
  create_raspi_poller_job()
  eventlet.wsgi.server(eventlet.listen((get_hostname(), SOCKET_IO_SERVER_PORT)), app)
  