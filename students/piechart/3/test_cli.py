from cli import (
    ls,
    mk,
    rm,
    contains,
    since,
)

import pytest

@pytest.fixture
def earlier_than_now_timestamp():
    from datetime import datetime
    return int(datetime.timestamp(datetime.now())) - 10

def test_ls_empty_dir(tmp_path):
    assert ls(tmp_path) == []

def test_ls_only_dirs(tmp_path):
    d = tmp_path / 'another_dir'
    d.mkdir()
    assert len(ls(tmp_path)) == 1

def test_ls_only_files(tmp_path):
    f = tmp_path / 'file.txt'
    f.write_text('text')
    assert f.read_text() == 'text'
    assert len(ls(tmp_path)) == 1

def test_ls_files_and_dirs(tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    f = tmp_path / 'file.txt'
    f.write_text('text')
    assert(len(ls(tmp_path))) == 2

def test_mk_no_filename():
    assert mk() == 'wrong argument'

def test_mk_en_filename(tmp_path):
    f = tmp_path / 'file.txt'
    assert mk(f) == 'success'

def test_mk_ru_filename(tmp_path):
    f = tmp_path / 'файл.txt'
    assert mk(f) == 'success'

def test_mk_duplicate(tmp_path):
    f = tmp_path / 'file.txt'
    f.write_text('text')
    assert mk(f) == 'file already exists'

def test_mk_invalid_filename(tmp_path):
    f = tmp_path / 'f/1/l/e.txt'
    assert mk(f) == 'invalid filename'

def test_rm_success(tmp_path):
    f = tmp_path / 'file.txt'
    f.write_text('text')
    assert rm(f) == 'success'

def test_rm_dir(tmp_path):
    d = tmp_path / 'dir'
    d.mkdir()
    assert rm(d) == 'argument is dir'

def test_rm_fail(tmp_path):
    f = tmp_path / 'somefile.txt'
    assert rm(f) == 'file not found'

def test_rm_no_filename():
    assert rm() == 'wrong argument'

def test_contains_no_filename():
    assert contains() == 'wrong argument'

def test_contains_success():
    mk('file.txt')
    assert contains('file.txt') == 0
    rm('file.txt')

def test_contains_dir(tmp_path):
    d = tmp_path / 'dir'
    d.mkdir()
    assert contains(d) == 'argument is dir'

def test_contains_non_existing_file():
    assert contains('non_existing_file.txt') == 1

def test_since_no_date():
    assert since() == 'wrong argument'

def test_since_not_existing_dir(tmp_path):
    d = tmp_path / 'dir'
    assert since(123, d) == 'dir not found'

def test_since_empty_dir(tmp_path):
    d = tmp_path / 'dir'
    d.mkdir()
    assert since(123, d) == 'dir is empty'

def test_since_only_dirs(tmp_path, earlier_than_now_timestamp):
    d = tmp_path / 'dir'
    d.mkdir()
    ad = d / 'another dir'
    ad.mkdir()
    result = since(earlier_than_now_timestamp, d)
    assert isinstance(result, list)
    assert len(result) == 1

def test_since_only_files(tmp_path, earlier_than_now_timestamp):
    d = tmp_path / 'dir'
    d.mkdir()
    f = d / 'file.txt'
    f.write_text('test')
    result = since(earlier_than_now_timestamp, d)
    assert isinstance(result, list)
    assert len(result) == 1

def test_since_dirs_and_files(tmp_path, earlier_than_now_timestamp):
    d = tmp_path / 'dir'
    d.mkdir()
    subdir = d / 'subdir'
    subdir.mkdir()
    f = d / 'file.txt'
    f.write_text('text')
    result = since(earlier_than_now_timestamp, d)
    assert isinstance(result, list)
    assert len(result) == 2

def test_since_invalid_date():
    assert since('abcd') == 'wrong argument'
