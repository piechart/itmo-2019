# -*- coding: utf-8 -*-

import datetime

import pytest
import os  # noqa I001
import shutil  # noqa I001

EMPTY_STR = ''
FILE_STR = 'file.txt'
DOT = '.'
DIR_STR = 'dir'
WRONG_ARG_STR = 'WRONG_ARGUMENT'


@pytest.fixture
def earlier_than_now_timestamp():
    """Timestamp."""
    return int(datetime.datetime.timestamp(datetime.datetime.now())) - 10


@pytest.fixture(params=[
    ('empty', [], 0),
    ('only_dirs', [DIR_STR], 1),
    ('only_files', [FILE_STR], 1),
    ('dirs_and_files', [DIR_STR, FILE_STR], 2),
])
def ls_fixture(tmp_path, request):
    """Fixture."""
    work_dir = tmp_path / request.param[0]
    paths, result_count = request.param[1], request.param[2]
    work_dir.mkdir()
    for path in paths:
        current_object = work_dir / path
        if DOT in path:
            current_object.write_text(EMPTY_STR)
        else:
            current_object.mkdir()
    yield (work_dir, result_count)


@pytest.fixture(params=[
    (EMPTY_STR, WRONG_ARG_STR, False),
    (FILE_STR, 'ok', True),
    ('файл.txt', 'ok', True),
    ('f/1/l/e.txt', 'INVALID_FILENAME', True),
    ('cli.py', 'FILE_EXISTS', False),
])
def mk_fixture(tmp_path, request):
    """Fixture mk."""
    yield request.param


@pytest.fixture(params=[
    (DIR_STR, 'ARG_IS_DIR', True),
    (FILE_STR, 'FILE_NOT_FOUND', False),
    (EMPTY_STR, WRONG_ARG_STR, 'False'),
    (FILE_STR, 'ok', True),
])
def rm_fixture(tmp_path, request):
    """Fixture rm."""
    path, expected_result, should_create = request.param
    final_path = path
    is_file = DOT in final_path
    if final_path and should_create:
        final_path = tmp_path / path
        final_path.write_text(EMPTY_STR) if is_file else final_path.mkdir()  # noqa WPS428
    yield (final_path, expected_result)


@pytest.fixture(params=[
    (EMPTY_STR, WRONG_ARG_STR, False),
    (FILE_STR, 0, True),
    (DIR_STR, 'ARG_IS_DIR', True),
    (FILE_STR, 1, False),
])
def contains_fixture(request):
    """Contains fixture."""
    path, expected_result, should_create = request.param
    is_file = DOT in path
    if path and should_create:
        if is_file and not os.path.exists(path):
            open(path, 'a').close()  # noqa WPS515
        else:
            os.mkdir(path)
    yield (path, expected_result)
    if should_create:
        shutil.rmtree(path) if not is_file else os.remove(path)  # noqa WPS441, WPS428


@pytest.fixture(params=[  # noqa C901
    ([None], WRONG_ARG_STR, False),
    ([DIR_STR], 'DIR_NOT_FOUND', False),
    ([DIR_STR], 'DIR_IS_EMPTY', True),
    (['dir/another dir'], ['another dir'], True),
    (['dir/file.txt'], [FILE_STR], True),
    (['dir/subdir', 'dir/file.txt'], [FILE_STR, 'subdir'], True),
])
def since_fixture(request, earlier_than_now_timestamp):  # noqa WPS442
    """Since fixture."""
    paths, expected_result, should_create = request.param
    work_dir = paths[0]
    if work_dir and should_create:
        if '/' in work_dir:
            work_dir = work_dir.split('/')[0]
        os.mkdir(work_dir)
    if should_create:
        for path in paths:
            if path and not os.path.exists(path):
                is_file = DOT in path
                if is_file:
                    open(path, 'a').close()  # noqa WPS515
                else:
                    os.mkdir(path)
    yield (work_dir, earlier_than_now_timestamp, expected_result)
    if should_create:
        for another_path in paths:  # noqa WPS440
            if another_path:
                if DOT in another_path:
                    os.remove(another_path)
                else:
                    shutil.rmtree(another_path)
    if work_dir and os.path.exists(work_dir):
        shutil.rmtree(work_dir)


@pytest.fixture(params=[
    ('ls', EMPTY_STR),
    ('mk', FILE_STR),
    ('contains', FILE_STR),
    ('since', earlier_than_now_timestamp),
    ('rm', FILE_STR),
])
def integration_fixture(request):
    """Fixture."""
    yield request.param
