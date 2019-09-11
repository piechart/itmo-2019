from factorial import find_factorial


def test_factorial():

    assert find_factorial(1) == 1

    assert find_factorial(5) == 120

    assert find_factorial(-1) is None

    assert find_factorial(0.6) is None


if __name__ == "__main__":
    test_factorial()