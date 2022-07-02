import argparse
import json
import os

from ..config import ACTIVE_PROCESSES_PATH

def read_active_processes():
    if not os.path.exists(ACTIVE_PROCESSES_PATH):
        return {}
    with open(ACTIVE_PROCESSES_PATH, 'r') as f:
        return json.load(f)
    
def save_active_processes(process: dict):
    with open(ACTIVE_PROCESSES_PATH, 'w') as f:
        return json.dump(process, f)

def set_process_id(process_name, process_id):
    processes = read_active_processes()
    processes[process_name] = process_id

    save_active_processes(processes)


def get_process_id(process_name):
    processes = read_active_processes()
    if not process_name in processes:
        return -1

    return processes[process_name]

def clear_process_by_name(process_name):
    processes = read_active_processes()
    if not process_name in processes:
        return

    del processes[process_name]
    save_active_processes(processes)

def clear_processes(process_name = None):
    if process_name is not None:
        return clear_process_by_name(process_name)
    if os.path.exists(ACTIVE_PROCESSES_PATH):
        os.remove(ACTIVE_PROCESSES_PATH)

# TODO: Log all actions
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gets or sets a process id')
    subparsers = parser.add_subparsers()

    parser_for_get_process = subparsers.add_parser('get')
    parser_for_get_process.add_argument('process_name', type=str)
    parser_for_get_process.set_defaults(func=get_process_id)

    parser_for_get_process = subparsers.add_parser('set')
    parser_for_get_process.add_argument('process_name', type=str)
    parser_for_get_process.add_argument('process_id', type=int)
    parser_for_get_process.set_defaults(func=set_process_id)

    parser_for_get_process = subparsers.add_parser('clear')
    parser_for_get_process.add_argument('process_name', type=str, nargs='?')
    parser_for_get_process.set_defaults(func=clear_processes)


    args = parser.parse_args()

    if args.func == get_process_id:
        print(args.func(args.process_name))
    elif args.func == set_process_id:
        args.func(args.process_name, args.process_id)
    elif args.func == clear_processes:
        args.func(args.process_name)
    else:
        raise Exception('No argument specified')
