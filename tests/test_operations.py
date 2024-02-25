from calculator.operations import add, divide, multiply, subtract


def test_add() -> None:
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-2, 2) == 0
    assert add(1, 2) == 3
    assert add(1, 5) == 6
    assert add(2, 5) == 7
    assert add(2, 4) == 6


def test_subtract() -> None:
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-2, 2) == -4
    assert subtract(-1, 2) == -3
    assert subtract(-1, 5) == -6
    assert subtract(-2, 5) == -7


def test_multiply() -> None:
    assert multiply(2, 3) == 6
    assert multiply(0, 10) == 0
    assert multiply(-2, 4) == -8
    assert multiply(-2, 5) == -10
    assert multiply(5, 6) == 30


def test_divide() -> None:
    assert divide(6, 3) == 2
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    assert divide(7, -2) == -3.5


if __name__ == "__main__":
    print("Running test_add()")
    test_add()
    print("Running test_subtract()")
    test_subtract()
    print("Running test_multiply()")
    test_multiply()
    print("Running test_divide()")
    test_divide()
