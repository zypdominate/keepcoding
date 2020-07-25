##  使用future处理并发

#### 1. 网络下载的三种风格

为了高效处理网络I/O，需要使用并发，因为网络有很高的延迟，所以为了不浪费CPU周期去等待，最好在收到网络响应之前做些其他的事。

两个示例程序，从网上下载图片。第一个示例程序是依序下载的：下载完一个图，并将其保存在硬盘中之后，才请求下一个图像。另一个脚本是并发下载的：几乎同时请求所有图像，每下载完一个文件就保存一个文件，脚本使用concurrent.futures模块。

**在I/O密集型应用中，如果代码写得正确，那么不管使用哪种并发策略（使用线程或asyncio包），吞吐量都比依序执行的代码高很多。**

```python
import os
import sys
import time
import requests

DOWNNLOAD_DIR = r'D:\downloadimage'
BASE_URL = 'http://pic2.sc.chinaz.com/Files/pic/pic9/202002/'
image_list = ['zzpic231' + str(i) + '_s.jpg' for i in range(50, 80)]

def save_image(img, filename):
    path = os.path.join(DOWNNLOAD_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

def get_image(suffix):
    url = os.path.join(BASE_URL, suffix)
    response = requests.get(url)
    return response.content

def show(text):
    print(text,end='\n')
    sys.stdout.flush()

def download_all(image_name_list):  # download_all是与并发实现比较的关键函数。
    for image_name in image_name_list:
        image = get_image(image_name)
        save_image(image, image_name)
        show(image)
    return len(image_name_list)

def main(download_task):
    t0 = time.time()
    count = download_task(image_list)
    elapsed = time.time() - t0
    msg = f'\n download {count} images in {elapsed}s'
    print(msg)

if __name__ == '__main__':
    main(download_all)

#  download 80 images in 4.6661295890808105s
#  download 80 images in 5.478628873825073s
#  download 80 images in 4.028514862060547s
```

---

#### 2. 使用concurrent.futures模块下载

concurrent.futures模块的主要特色是 **ThreadPoolExecutor** 和 **ProcessPoolExecutor** 类，这两个类实现的接口能分别在不同的线程或进程中执行可调用的对象。这两个类在内部维护着一个工作线程或进程池，以及要执行的任务队列。不过，这个接口抽象的层级很高，像下载国旗这种简单的案例，无需关心任何实现细节。

使用ThreadPoolExecutor.map方法，以最简单的方式实现并发下载：

```python
from concurrent import futures
from a5_4_downloadimage import save_image, get_image, show, main

MAX_WORDERS = 20  # 设定ThreadPoolExecutor类最多使用几个线程：并发20个

def download_single(image_name):
    image = get_image(image_name)
    save_image(image, image_name)
    show(image)
    return image_name

def download_multiple(image_name_list):
    tasks = min(MAX_WORDERS, len(image_name_list))
    with futures.ThreadPoolExecutor(tasks) as executor:
        res = executor.map(download_single, sorted(image_name_list))
    return len(list(res))

if __name__ == '__main__':
    main(download_multiple)

# download 80 images in 1.4081335067749023s
# download 80 images in 1.561039924621582s
# download 80 images in 1.393141746520996s
```

download_multiple 函数中设定工作的线程数量：使用允许的最大值（MAX_WORKERS）与要处理的数量之间较小的那个值，以免创建多余的线程；使用工作的线程数实例化ThreadPoolExecutor类；`executor.__exit__ ` 方法会调用 `executor.shutdown(wait=True)` 方法，它会在所有线程都执行完毕前阻塞线程；map方法的作用与内置的map函数类似，不过 download_single 函数会在多个线程中并发调用；map方法返回一个生成器，因此可以迭代，获取各个函数返回的值。最后返回获取的结果数量，如果有线程抛出异常，异常会在return语句处抛出，这与隐式调用 next() 函数从迭代器中获取相应的返回值一样。

download_single 函数其实是前面例子中的 download_all 函数的 for 循环体。**编写并发代码时经常这样重构：把依序执行的for循环体改成函数，以便并发调用。**

---

#### 3. 阻塞型IO和GIL

**CPython解释器本身就不是线程安全的，因此有全局解释器锁（GIL），一次只允许使用一个线程执行Python字节码。** 因此，一个Python进程通常不能同时使用多个CPU核心。

编写Python代码时无法控制GIL；不过，执行耗时的任务时，可以使用一个内置的函数或一个使用C语言编写的扩展释放GIL。其实，有个使用C语言编写的Python库能管理GIL，自行启动操作系统线程，利用全部可用的CPU核心。这样做会极大地增加库代码的复杂度，因此大多数库的作者都不这么做。

然而，标准库中所有执行阻塞型I/O操作的函数，在等待操作系统返回结果时都会释放GIL。这意味着在Python语言这个层次上可以使用多线程，而 **I/O密集型Python程序能从中受益：一个Python线程等待网络响应时，阻塞型I/O函数会释放GIL，再运行一个线程**。

Python标准库中的所有阻塞型I/O函数都会释放GIL，允许其他线程运行。time.sleep() 函数也会释放GIL。因此，尽管有GIL，Python线程还是能在I/O密集型应用中发挥作用。(常见的大部分任务都是I/O密集型任务，比如Web应用。)

---

#### 4. 使用concurrent.futures模块启动进程

concurrent.futures模块的文档副标题是“Launching parallel tasks”（执行并行任务）。这个模块实现的是真正的并行计算，因为它使用ProcessPoolExecutor类把工作分配给多个Python进程处理。因此，如果需要做CPU密集型处理，使用这个模块能绕开GIL，利用所有可用的CPU核心。

ProcessPoolExecutor和ThreadPoolExecutor类都实现了通用的Executor接口，因此使用concurrent.futures模块能特别轻松地把基于线程的方案转成基于进程的方案。

下载图片的示例或其他I/O密集型作业使用ProcessPoolExecutor类得不到任何好处。这一点易于验证，只需把示例中下面这几行：

```python
def download_multiple(image_name_list):
    tasks = min(MAX_WORDERS, len(image_name_list))
    with futures.ThreadPoolExecutor(tasks) as executor:
```

改成：

```python
def download_multiple(image_name_list):
		with futures.ProcessPoolExecutor() as executor:
```

对简单的用途来说，这两个实现Executor接口的类唯一值得注意的区别是，`ThreadPoolExecutor.__init__` 方法需要max_workers参数，指定线程池中线程的数量。在`ProcessPoolExecutor` 类中，那个参数是可选的，而且大多数情况下不使用——默认值是os.cpu_count() 函数返回的CPU数量。这样处理说得通，因为对CPU密集型的处理来说，不可能要求使用超过CPU数量的职程。而对I/O密集型处理来说，可以在一个 ThreadPoolExecutor 实例中使用10个、100个或1000个线程；最佳线程数取决于做的是什么事，以及可用内存有多少，因此要仔细测试才能找到最佳的线程数。

由于目前电脑配置非常低，经过几次测试，我发现使用ProcessPoolExecutor实例下载80张图片的时间增加到了一倍。ProcessPoolExecutor的价值主要还是体现在CPU密集型作业上。

---

#### 5. 实验Executor.map方法

若想并发运行多个可调用的对象，最简单的方式是使用前面示例中见过的Executor.map方法。

简单演示ThreadPoolExecutor类的map方法：

```python
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
```

创建 ThreadPoolExecutor 实例，有 3 个线程， 把五个任务提交给executor（因为只有3个线程，所以只有3个任务会立即开始：wait(0)、wait(1)和wait(2)），这是非阻塞调用。调用executor.map 方法的结果：一个生成器。for循环中的enumerate函数会隐式调用next(results)，这个函数又会在（内部）表示第一个任务（wait(0)）的 `_f` future上调用 `_f.result()` 方法。result方法会阻塞，直到future运行结束，因此这个循环每次迭代时都要等待下一个结果做好准备。

运行结果：

```
15:45:28 **********Starting**********
15:45:28  wait(0): doing nothing for 0s...
15:45:28  wait(0) done.
15:45:28 	 wait(1): doing nothing for 1s...
15:45:28 		 wait(2): doing nothing for 2s...
15:45:28 Result: <generator object Executor.map.<locals>.result_iterator at 0x000002307FF8C6D0>
15:45:28 			 wait(3): doing nothing for 3s...
15:45:28 Waitint for individual results:
15:45:28 result 0:<generator object Executor.map.<locals>.result_iterator at 0x000002307FF8C6D0>
15:45:29 	 wait(1) done.
15:45:29 				 wait(4): doing nothing for 4s...
15:45:29 result 1:<generator object Executor.map.<locals>.result_iterator at 0x000002307FF8C6D0>
15:45:30 		 wait(2) done.
15:45:30 					 wait(5): doing nothing for 5s...
15:45:30 result 2:<generator object Executor.map.<locals>.result_iterator at 0x000002307FF8C6D0>
15:45:31 			 wait(3) done.
15:45:31 result 3:<generator object Executor.map.<locals>.result_iterator at 0x000002307FF8C6D0>
15:45:33 				 wait(4) done.
15:45:33 result 4:<generator object Executor.map.<locals>.result_iterator at 0x000002307FF8C6D0>
15:45:35 					 wait(5) done.
15:45:35 result 5:<generator object Executor.map.<locals>.result_iterator at 0x000002307FF8C6D0>
```

