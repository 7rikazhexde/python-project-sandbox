from calculator.operations import add, divide, multiply, subtract


def test_add() -> None:
    print("Running test_add()")
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-2, 2) == 0
    assert add(1, 2) == 3
    assert add(1, 5) == 6
    assert add(2, 5) == 7
    assert add(2, 4) == 6


def test_subtract() -> None:
    print("Running test_subtract()")
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-2, 2) == -4
    assert subtract(-1, 2) == -3
    assert subtract(-1, 5) == -6
    assert subtract(-2, 5) == -7


def test_multiply() -> None:
    print("Running test_multiply()")
    assert multiply(2, 3) == 6
    assert multiply(0, 10) == 0
    assert multiply(-2, 4) == -8
    assert multiply(-2, 5) == -10
    assert multiply(5, 6) == 30


def test_divide() -> None:
    print("Running test_divide()")
    assert divide(6, 3) == 2
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    assert divide(7, -2) == -3.5
    assert divide(1, 1) == 1


if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
