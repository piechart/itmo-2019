# -*- coding: utf-8 -*-


def find_factorial(num):
    """
    This function finds a factorial of a given number a.

    If the given number is negative or non-integer, it returns None
    """
    if num < 0 or not isinstance(num, int):
        return None
    elif num == 1:
        return num
    return num * find_factorial(num - 1)
