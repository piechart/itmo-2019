# -*- coding: utf-8 -*-

import subprocess

from cli import ls, mk, rm, contains, since  # noqa: I001


def test_ls(fixture_ls):
    """Test ls function."""
    pathname, inside_contents = fixture_ls
    assert ls(pathname) == inside_contents


def test_mk(fixture_mk):
    """Test mk function."""
    filename, expected = fixture_mk
    with expected:
        mk(filename)


def test_rm(fixture_rm):
    """Test rm function."""
    _, filename, expected = fixture_rm
    with expected:
        rm(filename)


def test_contains(fixture_contains):
    """Test contains function."""
    _, filename, expected = fixture_contains
    assert contains(filename)['result'] == expected


def test_since(fixture_since):
    """Test since function."""
    pathname, inside_contents, time, expected = fixture_since
    with expected:
        assert since(pathname, time) == inside_contents


def test_integration(fixture_integration):
    """Integration test."""
    command, argument, exit_code = fixture_integration
    assert subprocess.call(
        ['python', '{0}.py'.format(command), argument],
        shell=True,  # noqa: S602
    ) == exit_code
