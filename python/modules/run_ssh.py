import subprocess
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection


def start_ssh_request(hostname, commands, send_output=None):
  # print('send_output', send_output)
  print_fn = send_output if send_output is not None else print
  print_fn(f'ssh {hostname} {commands}')
  ssh = subprocess.Popen(["ssh", hostname],
                          stdin =subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True,
                          bufsize=0)
  
  for command in commands:
    ssh.stdin.write('{}\n'.format(command))
  ssh.stdin.close()

  stdout = list(ssh.stdout)
  stderr = list(ssh.stderr)

  # print_fn('stdout')
  # for line in stdout:
  #   print_fn('line')
  #   print_fn(line)
  # print_fn('stderr')
  # for line in stderr:
  #   print_fn('line')
  #   print_fn(line)
  # print('ssh.stdout', list(ssh.stdout))
  # print('ssh.stdout', len(list(ssh.stdout)))
  # print('ssh.stderr', len(list(ssh.stderr)))
  # print('list(ssh.stderr)', list(ssh.stderr))
  # for line in list(ssh.stderr):
  #     print('\t line: ', line.strip())

  return ssh

def run_ssh_on_seperate_process(hostname, commands, send_output=None):
  job = Process(
    target=start_ssh_request,
    args=(hostname, commands, send_output)
  )

  job.start()
  return job

def run_ssh(hostname: str, commands: list, send_output=None):
  # https://janakiev.com/blog/python-shell-commands/
  # https://gist.github.com/bortzmeyer/1284249
  return run_ssh_on_seperate_process(hostname, commands, send_output)
