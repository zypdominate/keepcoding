
import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        res = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        args_str = ', '.join(repr(arg) for arg in args)
        print(f'[{elapsed:>2.8}s], {name}({args_str})--> {res}')
        return res
    return clocked

