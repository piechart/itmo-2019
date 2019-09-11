def find_gcd(a, b):
    """ This function finds the Greatest Common Divisor of 2 numbers: a and b"""
    while b:
        # the right way
        # a, b = b, a % b

        # the bug
        a, b = b, a // b
    return a
