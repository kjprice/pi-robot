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

from modules.config import get_hostname

from run_image_processing_server import continuously_find_and_process_images
from run_camera_head import start_camera_process

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

  env_vars = {**os.environ, **env_vars}

  job = multiprocessing.Process(
    target=fn_reference,
    kwargs={'env': env_vars}
  )
  job.start()
  jobs_running_by_fn_name[fn_name] = job

def create_image_processing_server_job():
  create_job('continuously_find_and_process_images', continuously_find_and_process_images)

def create_camera_head_server_job():
  env_vars = {'IS_TEST': 'true'}
  create_job('start_camera_process', start_camera_process, env_vars=env_vars)

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': '../static/index.html',
    '/static': '../static/'
})

PORT = 9898

def create_homepage_url():
  return 'http://{}:{}/'.format(get_hostname(), PORT)

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

@sio.event
def my_message(sid, data):
    print('message ', data)

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
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen((get_hostname(), PORT)), app)