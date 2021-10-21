# TODO:
# - Give an option to run all the things - including:
#  - ssh or local camera head
#  - image processing-server
#  - servo server
# - Display images directly in browser

import os

import eventlet
import socketio


def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.config import get_hostname

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
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen((get_hostname(), PORT)), app)