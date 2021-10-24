# TODO:
# - Give an option to run all the things - including:
#  - ssh or local camera head
#  - image processing-server
#  - servo server
# - Display images directly in browser

import multiprocessing
import os

import eventlet
import socketio


def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.config import get_hostname, SOCKET_IO_SERVER_PORT, TEST_IMAGE_DIR

from run_image_processing_server import run_image_processing_server
from run_camera_head import start_camera_process

class JobProcess:
  job = None
  def __init__(self, fn_reference, env_vars):
    env_vars = {**os.environ, **env_vars}
    job = multiprocessing.Process(
      target=fn_reference,
      kwargs={'env': env_vars}
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

def create_job(fn_name, fn_reference, env_vars = {}):
  stop_job_if_exists_by_fn_name(fn_name)

  job = JobProcess(fn_reference, env_vars)

  jobs_running_by_fn_name[fn_name] = job

def create_image_processing_server_job():
  create_job('image_processing_server', run_image_processing_server)

def create_camera_head_server_job():
  env_vars = {'IS_TEST': 'true'}
  create_job('camera_head', start_camera_process, env_vars=env_vars)

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': '../static/index.html',
    '/static': '../static/'
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
def set_browser_room(sid):
  sio.enter_room(sid, BROWSERS_ROOM_NAME)
  print('setting client "{}" to room "{}"'.format(sid, BROWSERS_ROOM_NAME))

@sio.event
def load_all_servers(sid):
  sio.emit('all_servers_loading_status', { 'step': 1, 'details': 'create image processing server job' }, sid)
  create_image_processing_server_job()
  sio.emit('all_servers_loading_status', { 'step': 2, 'details': 'create camera head server job' }, sid)
  create_camera_head_server_job()
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
def output_image_processing_server(sid, message):
  sio.emit('output_image_processing_server', message, room=BROWSERS_ROOM_NAME)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
  eventlet.wsgi.server(eventlet.listen((get_hostname(), SOCKET_IO_SERVER_PORT)), app)