from typing import List

import subprocess
from multiprocessing import Process

from ...config import SERVER_NAMES
from ...server_module import ServerModule

class SSH_Process(ServerModule):
  hostname = None
  process_name = None
  commands = None
  flags = None
  def __init__(self, hostname: str, commands, process_name: str, flags: str, send_output = None) -> None:
    self.hostname = hostname
    self.process_name = process_name

    if flags is None:
      flags = []
    self.flags = flags
    self.commands = commands

    server_name = SERVER_NAMES.JOB_PROCESSER
    super().__init__(server_name, flags)
    self.start_threads()

  # TODO: We will want to also kill by port number (for servo server)
  def cleanup(self):
    # TODO: Update
    self.job = kill_process_by_name(self.hostname, self.process_name, self.flags)
  def terminate(self):
    self.job.terminate()
    self.cleanup()

  def run_continuously(self):
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

def run_ssh_process(hostname, commands, process_name, flags):
    job = Process(
      target=SSH_Process,
      args=(hostname, commands, process_name, flags)
    )
    job.start()

    return job

def start_process_by_name(hostname: str, process_name: str, flags):
  print('start_process_by_name', hostname, process_name)
  commands = [
      '~/Projects/pirobot/bin/run/start_process_by_name.sh {} "{}"'.format(process_name, flags)
  ]

  return run_ssh_process(hostname, commands, process_name, flags)


def kill_process_by_name(hostname: str, process_name: str, flags):
  print('kill_process_by_name', hostname, process_name)
  commands = [
      '~/Projects/pirobot/bin/misc/kill_process_by_name.sh {} "{}"'.format(process_name, flags)
  ]

  return run_ssh_process(hostname, commands, process_name, flags)
