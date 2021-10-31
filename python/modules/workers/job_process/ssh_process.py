from typing import List

from .job_process import JobProcess
from ...run_ssh import run_ssh

SCRIPT_PATH = '~/Projects/pirobot/bin'

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
      '{}.sh {}'.format(process_name, flags)
    ]

    self.job = run_ssh(hostname, commands)
  def cleanup(self):
    commands = [
      'cd {}'.format(SCRIPT_PATH),
      './kill_process_by_name.sh {}'.format(self.process_name)
    ]

    self.job = run_ssh(self.hostname, commands)
  def terminate(self):
    self.job.terminate()
    self.cleanup()

