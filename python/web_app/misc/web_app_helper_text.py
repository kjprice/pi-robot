from ...modules.config import get_hostname, SOCKET_IO_SERVER_PORT, get_local_ip

def create_homepage_url():
  return '\n'.join([
    '# Server URL',
    'http://{}:{}/'.format(get_hostname(), SOCKET_IO_SERVER_PORT)
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

def print_startup_details():
  print()
  print('**********')
  print()
  print(create_homepage_url())
  print()
  print(create_wsl_forward_helper_text())
  print()
  print('**********')
  print()
