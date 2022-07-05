from typing import List

import subprocess
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

from ...config import SERVER_NAMES
from .job_process import JobProcess
from ...server_module import ServerModule
from ...run_ssh import run_ssh

SCRIPT_PATH = '~/Projects/pirobot/bin'

def kill_process_by_name(hostname: str, process_name: str, send_output = None):
  print('kill_process_by_name', hostname, process_name)
  commands = [
    'cd {}'.format(SCRIPT_PATH),
    './misc/kill_process_by_name.sh {}'.format(process_name)
  ]

  return run_ssh(hostname, commands, send_output)

# TODO: This never calls `super`
class SSH_Process(ServerModule):
  hostname = None
  process_name = None
  commands = None
  def __init__(self, hostname: str, process_name: str, flags: str, send_output = None) -> None:
    print()
    print(hostname, process_name, flags)
    print()

    self.hostname = hostname
    self.process_name = process_name

    if flags is None:
      flags = []
    self.commands = [
      '~/Projects/pirobot/bin/run/start_process_by_name.sh {} "{}"'.format(process_name, flags)
    ]

    server_name = SERVER_NAMES.JOB_PROCESSER
    super().__init__(server_name, flags)
    self.start_threads()

    # self.job = run_ssh(hostname, commands, send_output)
  # TODO: We will want to also kill by port number (for servo server)
  def cleanup(self):
    # TODO: Update
    self.job = kill_process_by_name(self.hostname, self.process_name)
  def terminate(self):
    # TODO: Update
    self.job.terminate()
    self.cleanup()
  # async def transfer_std_out(self, stdout):
  #   for line in stdout:
  #     self.send_output(line)

  def run_continuously(self):
    import time
    time.sleep(5)
    # print_fn = send_output if send_output is not None else print
    self.send_output(f'ssh {self.hostname} {self.commands}')
    ssh = subprocess.Popen(["ssh", self.hostname],
                            stdin =subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            # stderr=subprocess.STDOUT,
                            universal_newlines=True,
                            bufsize=0)
    
    for command in self.commands:
      ssh.stdin.write('{}\n'.format(command))
    ssh.stdin.close()

    stdout = list(ssh.stdout)
    for line in stdout:
      self.send_output(line)

    stderr = list(ssh.stderr)
    for line in stderr:
      self.send_output(line)
