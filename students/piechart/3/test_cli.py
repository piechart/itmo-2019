# -*- coding: utf-8 -*-


import pytest
import subprocess

from cli import (
    contains,
    ls,
    mk,
    rm,
    since,
)

YES_THIS_IS_MAGIC_NUMBER = 123


@pytest.fixture
def earlier_than_now_timestamp():
    """Timestamp."""
    from datetime import datetime  # noqa WPS433
    return int(datetime.timestamp(datetime.now())) - 10


def test_ls_empty_dir(tmp_path):
    """Test func."""
    assert not ls(tmp_path)


def test_ls_only_dirs(tmp_path):
    """Test func."""
    directory = tmp_path / 'another_dir'
    directory.mkdir()
    assert len(ls(tmp_path)) == 1


def test_ls_only_files(tmp_path):
    """Test func."""
    filename = tmp_path / 'file.txt'
    filename.write_text('text')
    assert filename.read_text() == 'text'
    assert len(ls(tmp_path)) == 1


def test_ls_files_and_dirs(tmp_path):
    """Test func."""
    directory = tmp_path / 'sub'
    directory.mkdir()
    filename = tmp_path / 'file.txt'
    filename.write_text('text')
    assert len(ls(tmp_path)) == 2


def test_ls_integration():
    """Test func."""
    assert subprocess.call(['python3', 'cli.py', 'ls']) == 0


def test_mk_no_filename():
    """Test func."""
    assert mk() == 'wrong argument'


def test_mk_en_filename(tmp_path):
    """Test func."""
    filename = tmp_path / 'file.txt'
    assert mk(filename) == 'success'


def test_mk_ru_filename(tmp_path):
    """Test func."""
    filename = tmp_path / 'файл.txt'
    assert mk(filename) == 'success'


def test_mk_integration():
    """Test func."""
    assert subprocess.call(['python3', 'cli.py', 'mk', 'file.txt']) == 0


def test_mk_duplicate(tmp_path):
    """Test func."""
    filename = tmp_path / 'file.txt'
    filename.write_text('text')
    assert mk(filename) == 'file already exists'


def test_mk_invalid_filename(tmp_path):
    """Test func."""
    filename = tmp_path / 'f/1/l/e.txt'
    assert mk(filename) == 'invalid filename'


def test_rm_success(tmp_path):
    """Test func."""
    filename = tmp_path / 'file.txt'
    filename.write_text('text')
    assert rm(filename) == 'success'


def test_rm_dir(tmp_path):
    """Test func."""
    directory = tmp_path / 'dir'
    directory.mkdir()  # noqa WPS204
    assert rm(directory) == 'argument is dir'


def test_rm_fail(tmp_path):
    """Test func."""
    filename = tmp_path / 'somefile.txt'
    assert rm(filename) == 'file not found'


def test_rm_no_filename():
    """Test func."""
    assert rm() == 'wrong argument'


def test_rm_integration():
    """Test func."""
    assert subprocess.call(['python3', 'cli.py', 'rm', 'somefile.txt']) == 0


def test_contains_no_filename():
    """Test func."""
    assert contains() == 'wrong argument'


def test_contains_success():
    """Test func."""
    mk('file.txt')
    assert contains('file.txt') == 0
    rm('file.txt')


def test_contains_dir(tmp_path):
    """Test func."""
    directory = tmp_path / 'dir'
    directory.mkdir()  # noqa WPS204
    assert contains(directory) == 'argument is dir'


def test_contains_non_existing_file():
    """Test func."""
    assert contains('non_existing_file.txt') == 1


def test_since_no_date():
    """Test func."""
    assert since() == 'wrong argument'


def test_contains_integration():
    """Test func."""
    assert subprocess.call(['python3', 'cli.py', 'contains', 'file.txt']) == 0


def test_since_not_existing_dir(tmp_path):
    """Test func."""
    directory = tmp_path / 'dir'
    assert since(YES_THIS_IS_MAGIC_NUMBER, directory) == 'dir not found'


def test_since_empty_dir(tmp_path):
    """Test func."""
    directory = tmp_path / 'dir'
    directory.mkdir()
    assert since(YES_THIS_IS_MAGIC_NUMBER, directory) == 'dir is empty'


def test_since_only_dirs(tmp_path, earlier_than_now_timestamp):  # noqa WPS442
    """Test func."""
    directory = tmp_path / 'dir'
    directory.mkdir()
    adirectory = directory / 'another dir'
    adirectory.mkdir()
    func_result = since(earlier_than_now_timestamp, directory)
    assert isinstance(func_result, list)
    assert len(func_result) == 1


def test_since_only_files(tmp_path, earlier_than_now_timestamp):  # noqa WPS442
    """Test func."""
    directory = tmp_path / 'dir'
    directory.mkdir()
    filename = directory / 'file.txt'
    filename.write_text('test')
    func_result = since(earlier_than_now_timestamp, directory)
    assert isinstance(func_result, list)
    assert len(func_result) == 1


def test_since_dirs_and_files(tmp_path, earlier_than_now_timestamp):  # noqa WPS442
    """Test func."""
    directory = tmp_path / 'dir'
    directory.mkdir()
    subdir = directory / 'subdir'
    subdir.mkdir()
    filename = directory / 'file.txt'
    filename.write_text('text')
    func_result = since(earlier_than_now_timestamp, directory)
    assert isinstance(func_result, list)
    assert len(func_result) == 2


def test_since_integration():
    """Test func."""
    assert subprocess.call(['python3', 'cli.py', 'since', '0']) == 0


def test_since_invalid_date():
    """Test func."""
    assert since('abcd') == 'wrong argument'
