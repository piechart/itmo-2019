def find_factorial(a):
    """ This function finds a factorial of a given number a
    If the given number is negative or non-integer, it returns None"""
    if a < 0 or not isinstance(a, int):
        return None
    elif a == 1:
        return a
    return a * find_factorial(a-1)