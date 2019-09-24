import argparse
import os
import sys

def main(commands, module):
    if hasattr(module, commands[0]):
        getattr(module, commands[0])(commands[1:])
    else:
        print('Unknown command passed')

def ls(*args):
    d = os.getcwd() if not args[0] else args[0]
    files = [f.name for f in os.scandir(d) if f.is_file()]
    dirs = [folder.name for folder in os.scandir(d) if folder.is_dir()]
    return files + dirs

def mk(*args):
    if not args:
        return 1
    filename = args[0]
    if not filename:
        return 1
    if os.path.exists(filename):
        return 2

    try:
        open(filename, 'a').close()
    except OSError: # invalid filename
        return 3
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, nargs='*', help='Command to execute')
    args = parser.parse_args()

    current_module = sys.modules[__name__]
    main(args.command, current_module)
