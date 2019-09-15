#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import runtests


def test_correct_module_import():
    assert runtests.import_module(
        '{0}/{1}'.format(os.getcwd(), 'file_with_tests.py'),
    )


def test_incorrect_module_import():
    assert (not runtests.import_module('non_existing_file.py'))


def test_find_valid_files():
    assert runtests.find_files(
        os.getcwd(), '*{0}'.format(runtests.PY_EXTENSION),
    )


def test_find_invalid_files():
    assert (not runtests.find_files(os.getcwd(), '*.invalidExtension'))


def test_extract_tests():
    module = runtests.import_module(
        '{0}/{1}'.format(os.getcwd(), 'file_with_tests.py'),
    )
    assert runtests.extract_tests(module)
    assert (not runtests.extract_tests(None))
