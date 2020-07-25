from time import sleep, strftime
from concurrent import futures


def display(*args):
    print(strftime('%H:%M:%S'), end=' ')
    print(*args)


def wait(n):
    msg = '{} wait({}): doing nothing for {}s...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{} wait({}) done.'
    display(msg.format('\t' * n, n))
    return n * 10


def main():
    display('**********Starting**********')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(wait, range(6))
    display('Result:', results)
    display('Waitint for individual results:')
    for i, result in enumerate(results):
        display('result {}:{}'.format(i, results))

if __name__ == '__main__':
    main()