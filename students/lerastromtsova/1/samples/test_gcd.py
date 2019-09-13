# -*- coding: utf-8 -*-

from gcd import find_gcd

RAND_NUM1 = -20
RAND_NUM2 = 90


def test_gcd():
    """Test the gcd function."""
    assert find_gcd(1, 6) == 1  # noqa: S101

    assert find_gcd(0, 9) == 9  # noqa: S101

    assert find_gcd(RAND_NUM1, RAND_NUM2) == 10  # noqa: S101


if __name__ == '__main__':
    test_gcd()
