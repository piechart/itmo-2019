# -*- coding: utf-8 -*-

import subprocess

from cli import contains, ls, mk, rm, since


def test_ls(ls_fixture):
    """Test func."""
    work_dir, result_count = ls_fixture
    assert len(ls(work_dir)) == result_count


def test_mk(tmp_path, mk_fixture):
    """Test func."""
    filename, expected_result, add_temp_path = mk_fixture
    full_path = tmp_path / filename if add_temp_path else filename
    assert mk(full_path) == expected_result


def test_rm(rm_fixture):
    """Test func."""
    path, expected_result = rm_fixture
    assert rm(path) == expected_result


def test_contains(contains_fixture):
    """Test func."""
    path, expected_result = contains_fixture
    assert contains(path) == expected_result


def test_since(since_fixture):
    """Test func."""
    work_dir, date_arg, expected_result = since_fixture
    assert since(date_arg, work_dir) == expected_result


def test_integration(integration_fixture):
    """Test func."""
    command, arg = integration_fixture
    # format_str = 'python students/piechart/3/cli.py {0}'  # noqa E800
    format_str = 'python3 students/piechart/3/cli.py {0}'  # noqa E800
    command_str = format_str.format(command)
    assert subprocess.call(command_str, shell=True) == 0  # noqa: S602
