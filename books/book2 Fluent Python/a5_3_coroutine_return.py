from collections import namedtuple

Result = namedtuple('Result', 'count average')


def average():
    total, count = 0, 0
    _avg = None
    while True:
        var = yield
        if var is None:
            break
        total += var
        count += 1
        _avg = total / count
    return Result(count, _avg)


if __name__ == '__main__':

    avg = average()
    avg.send(None)
    avg.send(1)
    avg.send(2)
    avg.send(3)
    try:
        avg.send(None)
    except StopIteration as e:
        print(e)
