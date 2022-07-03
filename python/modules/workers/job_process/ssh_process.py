from typing import List

from .job_process import JobProcess
from ...run_ssh import run_ssh

SCRIPT_PATH = '~/Projects/pirobot/bin'

def kill_process_by_name(hostname: str, process_name: str):
  print('kill_process_by_name', hostname, process_name)
  commands = [
    'cd {}'.format(SCRIPT_PATH),
    './misc/kill_process_by_name.sh {}'.format(process_name)
  ]

  return run_ssh(hostname, commands)

class SSH_Process(JobProcess):
  hostname = None
  process_name = None
  def __init__(self, hostname: str, process_name: str, flags: str) -> None:
    print()
    print(hostname, process_name, flags)
    print()

    self.hostname = hostname
    self.process_name = process_name

    if flags is None:
      flags = []
    commands = [
      '~/Projects/pirobot/bin/run/start_process_by_name.sh {} "{}"'.format(process_name, flags)
    ]

    self.job = run_ssh(hostname, commands)
  # TODO: We will want to also kill by port number (for servo server)
  def cleanup(self):
    self.job = kill_process_by_name(self.hostname, self.process_name)
  def terminate(self):
    self.job.terminate()
    self.cleanup()

