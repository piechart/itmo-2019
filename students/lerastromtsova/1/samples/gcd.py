# -*- coding: utf-8 -*-


def find_gcd(num1, num2):
    """
    This function should find Greatest Common Divisor of 2 numbers.

    But it has a bug and fails the tests
    """
    while num2:
        num1, num2 = num2, num1 // num2
    return num1
