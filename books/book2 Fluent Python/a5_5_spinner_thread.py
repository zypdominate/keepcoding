import itertools
import sys
import threading
import time


class Signal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  # 使用退格符（\x08）把光标移回来
        time.sleep(0.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))


def slow_function():
    # pretend to wait for I/O duration
    # 调用sleep函数会阻塞主线程，不过一定要这么做，以便释放GIL，创建从属线程。
    time.sleep(3)
    return 100


def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=("thinking...", signal))
    print(f"spinner object: {spinner}")
    spinner.start()
    ret = slow_function()
    signal.go = False
    spinner.join()
    return ret


if __name__ == '__main__':
    supervisor()
