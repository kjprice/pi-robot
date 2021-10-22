"""
This allows communication with the web-app (if it is online)
"""

import socketio

try:
    from modules.config import SOCKET_ROOMS, SOCKET_IO_HOST_URI
except ModuleNotFoundError:
    from config import SOCKET_ROOMS, SOCKET_IO_HOST_URI

class SocketCommunicationsNamespace(socketio.ClientNamespace):
  def __init__(self, namespace, socket_hub):
    self.socket_hub = socket_hub
    super().__init__(namespace=namespace)
  def on_connect(self):
    self.socket_hub.on_connect()

  def on_disconnect(self):
    self.socket_hub.on_disconnect()

  # TODO: This is not working - not receiving a response yet
  def on_my_event(self, data):
    print()
    print('HEY! I GOT A RESPONES')
    print()
    self.emit('my_response', data)


class SocketCommunications:
  connected = False
  socket_namespace = None
  namespace_str = None
  sio = None

  def __init__(self, namespace) -> None:
    sio = self.sio = socketio.Client()
    if not namespace in SOCKET_ROOMS:
      raise ValueError('Received "{}" but expected namespace to be one of: '.format(namespace), SOCKET_ROOMS)
    
    print('Trying to connect to socket server as "{}"'.format(namespace))
    self.namespace_str = namespace_str = '/{}'.format(namespace)
    self.socket_namespace = socket_namespace = SocketCommunicationsNamespace(namespace_str, self)
    sio.register_namespace(socket_namespace)
    try:
      sio.connect(SOCKET_IO_HOST_URI)
      self.connected = True
    except socketio.exceptions.ConnectionError:
      print('could not connect to socket')
      self.connected = False

  def on_connect(self):
    print('yay! connected!')

  def on_disconnect(self):
    self.connected = False
  
  def emit(self, message, data):
    if not self.connected:
      return
    self.socket_namespace.emit(message, data)
