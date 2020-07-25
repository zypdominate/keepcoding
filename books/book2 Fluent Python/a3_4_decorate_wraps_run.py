import time
from a3_4_decorate_wraps import clock


@clock
def test_sleep(seconds, name=None):
    time.sleep(seconds)


@clock
def test_factorial(n, name="fi"):
    return 1 if n < 2 else n * test_factorial(n - 1)


if __name__ == '__main__':
    test_sleep(1.2, name='xiaoming')
    test_factorial(5, name='fi')
