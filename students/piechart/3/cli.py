# -*- coding: utf-8 -*-

import argparse
import os
import sys

WRONG_ARGUMENT = 'WRONG_ARGUMENT'


def main(commands, module):
    """Main."""
    executable = commands[0]
    supported = {
        'ls': ls,
        'mk': mk,
        'rm': rm,
        'contains': contains,
        'since': since,
    }
    if executable in supported:
        func_to_execute = supported[executable]
        arg = commands[1] if len(commands) > 1 else None
        func_to_execute(arg)
    else:
        print('You better use supported command, human')  # noqa T001


def ls(arg=None):
    """ls."""
    directory = os.getcwd() if arg is None else arg
    scan_result = os.scandir(directory)
    files_filtered = filter(lambda zxc: zxc.is_file(), scan_result)
    files_mapped = list(map(lambda zxc: zxc.name, files_filtered))
    dirs = [folder.name for folder in os.scandir(directory) if folder.is_dir()]
    return files_mapped + dirs


def mk(arg=None):
    """mk."""
    if not arg:
        return WRONG_ARGUMENT
    if os.path.exists(arg):
        return 'FILE_EXISTS'
    try:
        open(arg, 'a').close()  # noqa WPS515
    except OSError:
        return 'INVALID_FILENAME'
    return 'ok'


def rm(arg=None):
    """rm."""
    if not arg:
        return 'WRONG_ARGUMENT'
    if os.path.isdir(arg):
        return 'ARG_IS_DIR'
    if not os.path.exists(arg):
        return 'FILE_NOT_FOUND'
    os.remove(arg)
    return 'ok'


def contains(arg=None):
    """contains."""
    if not arg:
        return WRONG_ARGUMENT
    if os.path.isdir(arg):
        return 'ARG_IS_DIR'
    result_list = ls()
    if arg in result_list:
        return 0
    return 1


def since(timestamp, directory=os.getcwd()):  # noqa WPS404, B008
    """since."""
    try:
        timestamp = int(timestamp)
    except Exception:
        return WRONG_ARGUMENT
    if not directory:
        return WRONG_ARGUMENT
    if not os.path.exists(directory):
        return 'DIR_NOT_FOUND'
    if not ls(directory):
        return 'DIR_IS_EMPTY'
    result_list = []
    for path in ls(directory):
        format_str = '{0}/{1}'
        formatted = format_str.format(directory, path)
        creation_time = os.stat(formatted).st_ctime
        if creation_time > timestamp:
            result_list.append(path)
    return result_list


def make_parser():
    """Arg parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('action', type=str, nargs='*', help='Action')
    return parser


if __name__ == '__main__':
    arguments = make_parser().parse_args()
    current_module = sys.modules[__name__]
    main(arguments.action, current_module)
