import argparse
import psutil

from .process_id import get_process_id

def kill_process_and_children(pid):
  parent = psutil.Process(pid)
  children = parent.children(recursive=True)
  for child in children:
    child.kill()
  parent.kill()
  parent.wait(5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kill a process (and children) by id or name')
    parser.add_argument('process_name_or_id', type=str)
    args = parser.parse_args()
    process_name_or_id = args.process_name_or_id

    process_id = None
    if process_name_or_id.isnumeric():
      process_id = int(process_name_or_id)
    else:
      process_id = get_process_id(process_name_or_id)
    kill_process_and_children(process_id)
