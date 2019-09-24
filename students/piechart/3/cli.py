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
        return 'wrong argument'
    if os.path.exists(arg):
        return 'file already exists'
    try:
        open(arg, 'a').close()
    except OSError:
        return 'invalid filename'
    return 'success'

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

def since(timestamp=None, directory=os.getcwd()):
    if not timestamp:
        return 'wrong argument'
    try:
        timestamp = int(timestamp)
    except:
        return 'wrong argument'
    if not os.path.exists(directory):
        return 'dir not found'
    content = ls(directory)
    if not content:
        return 'dir is empty'
    return [item for item in content if os.stat('{0}/{1}'.format(directory, item)).st_ctime > timestamp]



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, nargs='*', help='Command to execute')
    args = parser.parse_args()

    current_module = sys.modules[__name__]
    main(args.command, current_module)
