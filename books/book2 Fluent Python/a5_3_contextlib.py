from contextlib import contextmanager


@contextmanager
def lookingmirror():
    import sys

    oringin_write = sys.stdout.write

    def reverse_write(text):
        # 定义自定义的 reverse_write 函数；在闭包中可以访问 original_write。
        oringin_write(text[::-1])

    sys.stdout.write = reverse_write

    # 产出一个值，这个值会绑定到 with 语句中 as 子句的目标变量上。
    # 执行 with 块中的代码时，这个函数会在这一点暂停。
    msg = ''
    try:
        yield "lookingmirror func"
    except ZeroDivisionError as e:
        msg = e
    finally:
        # 控制权一旦跳出 with 块，继续执行 yield 语句之后的代码；
        # 这里是恢复成原来的 sys. stdout.write 方法。
        sys.stdout.write = oringin_write
        if msg:
            print(msg)


with lookingmirror() as l:
    print(l)
    print("12345")
