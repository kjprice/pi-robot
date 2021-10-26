# TODO:
# - Give an option to run all the things - including:
#  - ssh or local camera head
#  - image processing-server
#  - servo server

import multiprocessing
import os

import eventlet
import socketio


def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.config import get_hostname, SERVER_NAMES, SOCKET_IO_SERVER_PORT, SOCKET_ROOMS, STATIC_DIR, write_static_config

from run_image_processing_server import run_image_processing_server
from run_camera_head import start_camera_process

class JobProcess:
  job = None
  def __init__(self, fn_reference, env_vars, **kwargs):
    env_vars = {**os.environ, **env_vars}
    job = multiprocessing.Process(
      target=fn_reference,
      kwargs={'env': env_vars, **kwargs}
    )
    job.start()

    self.job = job
  def terminate(self):
    self.job.terminate()

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

def create_job(fn_name, fn_reference, env_vars = {}, **kwargs):
  stop_job_if_exists_by_fn_name(fn_name)

  job = JobProcess(fn_reference, env_vars, **kwargs)

  jobs_running_by_fn_name[fn_name] = job

def create_image_processing_server_job():
  server_name = SERVER_NAMES.IMAGE_PROCESSING.value
  create_job(server_name, run_image_processing_server)

def create_camera_head_server_job(**kwargs):
  env_vars = {'IS_TEST': 'true'}
  server_name = SERVER_NAMES.CAMERA_HEAD.value
  create_job(server_name, start_camera_process, env_vars=env_vars, **kwargs)

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': os.path.join(STATIC_DIR, 'index.html'),
    '/static': STATIC_DIR
})

def create_homepage_url():
  return 'http://{}:{}/'.format(get_hostname(), SOCKET_IO_SERVER_PORT)

print()
print('**********')
print()
print(create_homepage_url())
print()
print('**********')
print()

@sio.event
def connect(sid, environ):
  print('connect ', sid)

BROWSERS_ROOM_NAME = 'browsers'

@sio.event
def set_socket_room(sid, room_name):
  if not room_name in SOCKET_ROOMS:
    raise AssertionError('Expected room_name "{}" to be one of: {}'.format(room_name, SOCKET_ROOMS))

  sio.enter_room(sid, room_name)
  print('setting client "{}" to room "{}"'.format(sid, room_name))

@sio.event
def load_all_servers(sid, data):
  seconds_between_images = data['delay']
  sio.emit('all_servers_loading_status', { 'step': 1, 'details': 'create image processing server job' }, sid)
  create_image_processing_server_job()
  sio.emit('all_servers_loading_status', { 'step': 2, 'details': 'create camera head server job' }, sid)
  create_camera_head_server_job(seconds_between_images=seconds_between_images)
  sio.emit('all_servers_loading_status', { 'step': 3, 'details': 'complete' }, sid)

@sio.event
def stop_all_servers(sid):
  stop_all_server_processes()
  sio.emit('all_servers_stopped_status', to=sid)

@sio.event
def get_server_statuses(sid):
  jobs_running = jobs_running_by_fn_name.keys()
  sio.emit('browser_init_status', {'jobs_running': list(jobs_running)}, to=sid)

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
def delay_change(sid, delay_change):
  sio.emit('chnage_seconds_between_images', delay_change, room='camera_head')


@sio.event
def confirm_image_processing_server_online(sid):
  sio.emit('confirm_image_processing_server_online', room='camera_head')

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

def create_config_object():
  server_names = SERVER_NAMES.to_dict()

  return {
    'serverNames': server_names
  }

if __name__ == '__main__':
  write_static_config(create_config_object())
  eventlet.wsgi.server(eventlet.listen((get_hostname(), SOCKET_IO_SERVER_PORT)), app)