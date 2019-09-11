from gcd import find_gcd


def test_gcd():

    assert find_gcd(1, 6) == 1

    assert find_gcd(0, 9) == 9

    assert find_gcd(-20, 90) == 10


if __name__ == "__main__":
    test_gcd()