import time
from functools import wraps


def clock(func):
    @wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        args_list = []
        if args:
            args_list.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = [f'{k}={v}' for k, v in sorted(kwargs.items())]
            args_list.append(', '.join(pairs))
        args_str = ', '.join(args_list)
        print(f'[{elapsed:>2.8}s], {name}({args_str})--> {res}')
        return res

    return clocked
