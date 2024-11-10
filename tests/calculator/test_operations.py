from project_a.calculator.operations import add, divide, multiply, subtract


def test_add() -> None:
    print("Running test_add()")
    assert add(2, 1) == 3
    assert add(0, 0) == 0
    assert add(-2, 2) == 0
    assert add(1, 3) == 4
    assert add(1, -2) == -1
    assert add(100, 200) == 300
    assert add(-100, -200) == -300


def test_subtract() -> None:
    print("Running test_subtract()")
    assert subtract(5, 1) == 4
    assert subtract(0, 0) == 0
    assert subtract(-2, -2) == 0
    assert subtract(-1, 4) == -5
    assert subtract(-1, -4) == 3
    assert subtract(-1, -5001) == 5000


def test_multiply() -> None:
    print("Running test_multiply()")
    assert multiply(2, 3) == 6
    assert multiply(0, 10) == 0
    assert multiply(-2, 4) == -8
    assert multiply(-2, 5) == -10
    assert multiply(-1000, 5) == -5000


def test_divide() -> None:
    print("Running test_divide()")
    assert divide(6, 3) == 2
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    assert divide(7, -7) == -1
    assert divide(100, -2) == -50
