# -*- coding: utf-8 -*-

from factorial import find_factorial

RAND_NUM1 = 120
RAND_NUM2 = 0.6


def test_factorial():
    """Test the factorial function."""
    assert find_factorial(1) == 1  # noqa: S101

    assert find_factorial(5) == RAND_NUM1  # noqa: S101

    assert find_factorial(-1) is None  # noqa: S101

    assert find_factorial(RAND_NUM2) is None  # noqa: S101


if __name__ == '__main__':
    test_factorial()
