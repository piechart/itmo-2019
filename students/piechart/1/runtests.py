#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import imp
import os

PY_EXTENSION = '.py'
TEST_PREFIX = 'test_'


def find_files(directory, pattern):
    """Returns list of filepaths."""
    return glob.glob('{0}/{1}'.format(directory, pattern), recursive=True)


def import_module(target_file):
    """Returns either imported module or None."""
    name = os.path.basename(target_file).replace(PY_EXTENSION, '')

    if (not name) or (not os.path.exists(target_file)):
        return None

    return imp.load_source(name, target_file)


def extract_tests(module):
    """Returns either funcs dict or None."""
    if module is None:
        return None

    all_vars = vars(module).items()  # noqa: WPS421
    tests = filter(lambda elem: elem[0].startswith(TEST_PREFIX), all_vars)
    return dict(tests)


def execute_test(test_function):
    """Executes a function given."""
    try:
        test_function()
    except AssertionError:
        return 'fail'
    return 'ok'


def perform_testing(target_dir=''):
    """Looks up for tests in the directory given and performs its execution."""
    if not target_dir:
        target_dir = os.getcwd()

    for test_file in find_files(
        target_dir,
        '{0}*{1}'.format(TEST_PREFIX, PY_EXTENSION),
    ):
        module = import_module(test_file)

        if module is None:
            continue

        for test in (extract_tests(module) or {}).items():
            print('{0} - {1} - {2}'.format(  # noqa: T001
                test_file,
                test[0],
                execute_test(test[1]),
            ))


if __name__ == '__main__':
    target_dir = input('Input target dir (Enter for current): ')  # noqa: WPS421, S322, E501
    perform_testing(target_dir)
