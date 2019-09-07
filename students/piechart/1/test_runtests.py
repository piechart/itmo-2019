import os
import runtests


def test_correct_module_import():
    assert runtests.import_module(os.getcwd() + "/file_with_tests.py") != None


def test_incorrect_module_import():
    assert runtests.import_module("non_existing_file.py") == None


def test_find_valid_files():
    assert len(runtests.find_files(os.getcwd(), "*.py")) > 0


def test_find_invalid_files():
    assert len(runtests.find_files(os.getcwd(), "*.invalidExtension")) == 0


def test_extract_tests():
    module = runtests.import_module(os.getcwd() + "/file_with_tests.py")
    assert runtests.extract_tests(module) != None
    assert bool(runtests.extract_tests(module))  # not empty
    assert bool(runtests.extract_tests(None)) == False  # empty


test_correct_module_import()
test_incorrect_module_import()
test_find_valid_files()
test_find_invalid_files()
test_extract_tests()
