import argparse
import os
import sys

def main(commands, module):
    if hasattr(module, commands[0]):
        arg = commands[1] if len(commands) > 1 else None
        getattr(module, commands[0])(arg)
    else:
        print('Unknown command passed')

def ls(arg=None):
    d = os.getcwd() if arg is None else arg
    files = [f.name for f in os.scandir(d) if f.is_file()]
    dirs = [folder.name for folder in os.scandir(d) if folder.is_dir()]
    return files + dirs

def mk(arg=None):
    if not arg:
        return 1
    if os.path.exists(arg):
        return 2

    try:
        open(arg, 'a').close()
    except OSError: # invalid filename
        return 3
    return 0

def rm(arg=None):
    if not arg:
        return 'wrong argument'
    if os.path.isdir(arg):
        return 'argument is dir'
    if not os.path.exists(arg):
        return 'file not found'
    os.remove(arg)
    return 'success'

def contains(arg=None):
    if not arg:
        return 'wrong argument'
    if os.path.isdir(arg):
        return 'argument is dir'
    return 0 if arg in ls() else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, nargs='*', help='Command to execute')
    args = parser.parse_args()

    current_module = sys.modules[__name__]
    main(args.command, current_module)
