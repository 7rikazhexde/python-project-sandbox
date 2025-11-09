from typing import Union


def add(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """Add two numbers together."""
    return x + y


def subtract(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    return x - y


def multiply(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    return x * y


def divide(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    return x / y
