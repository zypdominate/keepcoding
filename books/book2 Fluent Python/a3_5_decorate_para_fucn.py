import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):  # clock 是参数化装饰器工厂函数。
    def decorate(func):
        def clocked(*args):
            t0 = time.time()
            _res = func(*args)
            result = repr(_res)
            elapsed = time.time() - t0
            name = func.__name__
            args_str = ', '.join(repr(arg) for arg in args)
            print(fmt.format(**locals()))
            return _res
        return clocked
    return decorate

if __name__ == '__main__':
    @clock()
    def snooze(seconds):
        time.sleep(seconds)
    # [0.12307549s] snooze((0.123,)) -> None

    # way2:
    @clock('{name}: {elapsed}s')
    def snooze(seconds):
        time.sleep(seconds)
    # snooze: 0.12392497062683105s

    # way3:
    @clock('{name}({args}) dt={elapsed:0.3f}s')
    def snooze(seconds):
        time.sleep(seconds)
    # snooze((0.123,)) dt=0.123s

    for i in range(3):
        snooze(.123)
        
