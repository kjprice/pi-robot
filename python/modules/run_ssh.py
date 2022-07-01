import subprocess
import multiprocessing

def start_ssh_request(hostname, commands):
  print(f'ssh {hostname} {commands}')
  ssh = subprocess.Popen(["ssh", hostname],
                          stdin =subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True,
                          bufsize=0)
  
  for command in commands:
    ssh.stdin.write('{}\n'.format(command))
  ssh.stdin.close()

  print('ssh.stdout', len(list(ssh.stdout)))
  for line in ssh.stdout:
      print(line.strip())
  print('ssh.stderr', len(list(ssh.stderr)))
  print('list(ssh.stderr)', list(ssh.stderr))
  for line in ssh.stderr:
      print('\t line: ', line.strip())

  return ssh

def run_ssh_on_seperate_process(hostname, commands):
  job = multiprocessing.Process(
    target=start_ssh_request,
    args=(hostname, commands)
  )

  job.start()
  return job

def run_ssh(hostname: str, commands: list):
  # https://janakiev.com/blog/python-shell-commands/
  # https://gist.github.com/bortzmeyer/1284249
  return run_ssh_on_seperate_process(hostname, commands)
