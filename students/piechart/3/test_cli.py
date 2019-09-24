import pytest
from cli import (
    ls,
    mk,
)

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
    assert mk() == 1

def test_mk_en_filename(tmp_path):
    f = tmp_path / 'file.txt'
    assert mk(f) == 0

def test_mk_ru_filename(tmp_path):
    f = tmp_path / 'файл.txt'
    assert mk(f) == 0

def test_mk_duplicate(tmp_path):
    f = tmp_path / 'file.txt'
    f.write_text('text')
    assert mk(f) == 2

def test_mk_invalid_filename(tmp_path):
    f = tmp_path / 'f/1/l/e.txt'
    assert mk(f) == 3
