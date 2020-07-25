from inspect import getgeneratorstate


class DemoException(BaseException):
    """为这次演示定义的异常类型。"""
    pass


def demo_exc_handling():
    print('-> coroutine started')
    try:
        while True:
            try:
                var = yield
            except DemoException as e:
                print('*** DemoException handled. Continuing...')
            else:
                print('-> coroutine received: {!r}'.format(var))
    finally:
        print('-> coroutine ending')



if __name__ == '__main__':

    cor_exc = demo_exc_handling()
    cor_exc.send(None)
    print(getgeneratorstate(cor_exc))  # GEN_SUSPENDED
    cor_exc.send(1)               # -> coroutine received: 1
    cor_exc.throw(DemoException)  # *** DemoException handled. Continuing...
    # 如果传入协程的异常没有处理，协程会停止，即状态变成'GEN_CLOSED'
    # cor_exc.throw(ZeroDivisionError)
    cor_exc.send(3)               # -> coroutine received: 3
    cor_exc.close()
    print(getgeneratorstate(cor_exc))  # GEN_CLOSED
