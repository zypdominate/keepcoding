# 普通计算移动平均值的协程
def average():
    total, count = 0, 0
    average = None
    while True:
        var = yield average
        total += var
        count += 1
        average = total / count


# 预激协程的装饰器
from functools import wraps

def coroutine(func):
    # 装饰器：向前执行到第一个yield表达式，预激func
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

@coroutine
def average_primer():
    total, count = 0, 0
    average = None
    while True:
        var = yield average
        total += var
        count += 1
        average = total / count


if __name__ == '__main__':

    avg = average()
    avg.send(None)  # next(avg)
    print(avg.send(1))
    print(avg.send(3))
    print(avg.send(5))

    # 预激协程的装饰器
    from inspect import getgeneratorstate
    avg_primer = average_primer()
    print(getgeneratorstate(avg_primer))  # GEN_SUSPENDED
    print(avg_primer.send(1))
    print(avg_primer.send(3))
    print(avg_primer.send(5))
