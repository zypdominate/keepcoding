import sys
import asyncio
import itertools


@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():
    yield from asyncio.sleep(3)
    return 100


@asyncio.coroutine
def supervisor():
    spinner = asyncio.async(spin('thinking...'))
    print(f"spinner object：{spinner}")
    ret = yield from slow_function()
    spinner.cancel()
    return ret


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()


if __name__ == '__main__':
    main()
