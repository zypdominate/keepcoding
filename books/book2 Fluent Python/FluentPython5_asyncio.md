##  使用asyncio包处理并发

#### 1. 线程与协程对比

在长时间计算的过程中，在控制台中显示一个由ASCII字符"|/-\"构成的动画旋转指针。一个借由 threading 模块使用线程实现，一个借由 asyncio 包使用协程实现。通过对比两种实现，理解如何不使用线程来实现并发行为。

```python
import sys
import time
import itertools
import threading

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

def show_function():
    # pretend to wait for I/O duration
    # 调用sleep函数会阻塞主线程，不过一定要这么做，以便释放GIL，创建从属线程。
    time.sleep(3)
    return 100

def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=("thinking...", signal))
    print(f"spinner object: {spinner}")
    spinner.start()
    ret = show_function()
    signal.go = False
    spinner.join()
    return ret


if __name__ == '__main__':
    supervisor()
```

Python没有提供终止线程的API，这是有意为之的。若想关闭线程，必须给线程发送消息。这里使用的是signal.go属性：在主线程中把它设为False后，spinner线程最终会注意到，然后干净地退出。

---

asyncio包使用的“协程”是较严格的定义。适合 asyncio API 的协程在定义体中必须使用 yield from，而不能使用 yield。此外，适合 asyncio 的协程要由调用方驱动，并由调用方通过 yield from 调用；或者把协程传给 asyncio 包中的某个函数，例如 asyncio.async(...) 和本章要介绍的其他函数，从而驱动协程。最后，@asyncio.coroutine 装饰器应该应用在协程上，如下述示例所示。

```python
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
            yield from asyncio.sleep(0.1)  # 这样的休眠不会阻塞事件循环
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))

@asyncio.coroutine
def slow_function():  # 现在，slow_function函数是协程；
    # 在用休眠假装进行I/O操作时，使用yield from继续执行事件循环
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
```

交给asyncio处理的协程要使用@asyncio.coroutine装饰。除非想阻塞主线程，从而冻结事件循环或整个应用，否则不要在asyncio协程中使用time.sleep(...)。如果协程需要在一段时间内什么也不做，应该使用yield fromasyncio.sleep(DELAY)。

使用@asyncio.coroutine装饰器不是强制要求，但是强烈建议这么做，因为这样能在一众普通的函数中把协程凸显出来，也有助于调试：如果还没从中产出值，协程就被垃圾回收了（意味着有操作未完成，因此有可能是个缺陷），那就可以发出警告。这个装饰器不会预激协程。

---

这两种supervisor实现之间的主要区别概述如下：

1. asyncio.Task对象差不多与threading.Thread对象等效。Task对象用于驱动协程，Thread对象用于调用可调用的对象。
2. Task对象不由自己动手实例化，而是通过把协程传给asyncio.async(...)函数或loop.create_task(...)方法获取。
3. 获取的Task对象已经排定了运行时间（例如，由asyncio.async函数排定）；Thread实例则必须调用start方法，明确告知让它运行。
4. 在线程版supervisor函数中，slow_function函数是普通的函数，直接由线程调用。在异步版supervisor函数中，slow_function函数是协程，由yield from驱动。
5. 没有API能从外部终止线程，因为线程随时可能被中断，导致系统处于无效状态。如果想终止任务，可以使用Task.cancel（　）实例方法，在协程内部抛出CancelledError异常。协程可以在暂停的yield处捕获这个异常，处理终止请求。
6. supervisor协程必须在main函数中由loop.run_until_complete方法执行。

---

#### 2. 使用asyncio和aiohttp包实现的异步下载图片

```python
import os
import asyncio
import aiohttp
from a5_4_downloadimage import BASE_URL, save_image, show, main

@asyncio.coroutine
def get_image(suffix):
    url = os.path.join(BASE_URL, suffix)
    # response = yield from aiohttp.request('GET', url)
    response = yield from aiohttp.ClientSession().get(url)
    image = yield from response.read()
    return image

@asyncio.coroutine
def download_one(img):
    image = yield from get_image(img)
    show(img)
    save_image(image, filename=img)
    return img

def download_all(image_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(img) for img in sorted(image_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)

if __name__ == '__main__':
    main(download_all)
    #  download 80 images in 1.0823283195495605s
```

