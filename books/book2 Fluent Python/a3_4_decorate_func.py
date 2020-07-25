import time
from a3_4_decorate import clock

@clock
def test_sleep(seconds):
    time.sleep(seconds)


@clock
def test_factorial(n):
    return 1 if n < 2 else n * test_factorial(n-1)


if __name__ == '__main__':
    test_sleep(1.2)
    test_factorial(6)
