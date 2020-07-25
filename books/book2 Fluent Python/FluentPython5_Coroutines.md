#### 1. 用作协程的生成器的基本行为

```python
def simple_coroutine():
    print("—> Coroutines started")
    var = yield   # 协程使用生成器函数定义：定义体中有yield关键字。
    print(f"—> Coroutines received {var}")
    
cor = simple_coroutine()

cor
Out[4]: <generator object simple_coroutine at 0x000001D368E8F410>
  
next(cor)  # 激活协程
—> Coroutines started

cor.send(123)
—> Coroutines received 123
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-6-3cd430c98ae0>", line 1, in <module>
    cor.send(123)
StopIteration
```

`var = yield`：yield在表达式中使用；如果协程只需从客户那里接收数据，那么产出的值是None——这个值是隐式指定的，因为yield关键字右边没有表达式。**首先要调用 `next(...)` 函数，因为生成器还没启动，没在yield语句处暂停，所以一开始无法发送数据**。

协程可以身处四个状态中的一个。当前状态可以使用 `inspect.getgeneratorstate(...)` 函数确定，该函数会返回下述字符串中的一个：

- 'GEN_CREATED'：等待开始执行；
- 'GEN_RUNNING'：解释器正在执行；
- 'GEN_SUSPENDED'：在yield表达式处暂停；
- 'GEN_CLOSED'：执行结束；

因为send方法的参数会成为暂停的yield表达式的值，所以，仅当协程处于暂停状态时才能调用send方法，例如cor.send(123)。不过，如果协程还没激活（即，状态是'GEN_CREATED'），情况就不同了。因此，**始终要调用next(cor)激活协程——也可以调用cor.send(None)**，效果一样。

```python
cor = simple_coroutine()
cor.send(None)  # 激活协程

# <generator object simple_coroutine at 0x000002601BE2E200>
# Coroutines started
```

如果创建协程对象后立即把None之外的值发给它，会出现下述错误：can't send non-None value to a just-started generator.

```python
cor = simple_coroutine()
cor.send(123)

Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-12-3cd430c98ae0>", line 1, in <module>
    cor.send(123)
TypeError: can't send non-None value to a just-started generator
```

最先调用 `next(cor)` 函数这一步通常称为“预激”（prime）协程（即，让协程向前执行到第一个yield表达式，准备好作为活跃的协程使用）。

---

```python
def simple_coroutine2(a):
    print(f"——> started a:{a}")
    b = yield a
    print(f"——> receiced b:{b}")
    c = yield a + b
    print(f"——> receiced c:{c}")

cor2 = simple_coroutine2(1)
print(getgeneratorstate(cor2))  # GEN_CREATED  协程未启动

cor2.send(None)
print(getgeneratorstate(cor2))  # GEN_SUSPENDED

print(cor2.send(2))
print(cor2.send(10))

'''
GEN_CREATED
——> started a:1
GEN_SUSPENDED
——> receiced b:2
3
——> receiced c:10
Traceback (most recent call last):
  File ".../a5_3_demo_coroutine.py", line 29, in <module>
    print(cor2.send(10))
StopIteration
'''
```

协程在yield关键字所在的位置暂停执行。在赋值语句中，=右边的代码在赋值之前执行。因此，对于`b=yield a` 这行代码来说，等到客户端代码再激活协程时才会设定b的值。

simple_coroutine2 协程的执行过程分为3个阶段：各个阶段都在yield表达式中结束，而且下一个阶段都从那一行代码开始，然后再把yield表达式的值赋给变量。

![image-20200308175931900](../../../markdown_pic/book2_coroutine_demo.png)

---

#### 2. 使用协程计算移动平均值

```python
def average():
    total, count = 0, 0
    average = None
    while True:
        var = yield average
        total += var
        count += 1
        average = total / count

avg = average()
avg.send(None)  # 预激协程

print(avg.send(1))
print(avg.send(3))
print(avg.send(5))
```

无限循环表明，只要调用方不断把值发给这个协程，它就会一直接收值，然后生成结果。仅当调用方在协程上调用.close（）方法，或者没有对协程的引用而被垃圾回收程序回收时，这个协程才会终止。这里的yield表达式用于暂停执行协程，把结果发给调用方；还用于接收调用方后面发给协程的值，恢复无限循环。

---

#### 3. 预激协程的装饰器

使用协程之前必须预激，可是这一步容易忘记。为了避免忘记，可以在协程上使用一个特殊的装饰器。

如果不预激，那么协程没什么用。调用my_coro.send(x)之前，记住一定要调用 next(my_coro) 或者my_coro.send(None) 。为了简化协程的用法，有时会使用一个预激装饰器。

```python
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
    from inspect import getgeneratorstate
    avg_primer = average_primer()
    print(getgeneratorstate(avg_primer))  # GEN_SUSPENDED
    print(avg_primer.send(1))
    print(avg_primer.send(3))
    print(avg_primer.send(5))
```

在 coroutine 函数中把被装饰的生成器函数替换成这里的 primer 函数，接着调用被装饰的函数，获取生成器对象，预激生成器，最后返回预激后的生成器。根据 getgeneratorstate 得到的状态为 GEN_SUSPENDED 可知，此时 avg_primer 状态已经不是 GEN_CREATED 协程未启动状态，而是在yield表达式处暂停。

---

#### 4. 终止协程和异常处理

协程中未处理的异常会向上冒泡，传给next函数或send方法的调用方（即触发协程的对象）。

客户代码可以在生成器对象上调用两个方法，显式地把异常发给协程。这两个方法是 **throw** 和**close** 。

`generator.throw(exc_type[, exc_value[, traceback]])` 致使生成器在暂停的yield表达式处抛出指定的异常。如果生成器处理了抛出的异常，代码会向前执行到下一个yield表达式，而产出的值会成为调用generator.throw方法得到的返回值。如果生成器没有处理抛出的异常，异常会向上冒泡，传到调用方的上下文中。

`generator.close（）` 致使生成器在暂停的yield表达式处抛出GeneratorExit异常。如果生成器没有处理这个异常，或者抛出了StopIteration异常（通常是指运行到结尾），调用方不会报错。如果收到GeneratorExit异常，生成器一定不能产出值，否则解释器会抛出RuntimeError异常。生成器抛出的其他异常会向上冒泡，传给调用方。

```python
from inspect import getgeneratorstate

class DemoException(BaseException):
    """为这次演示定义的异常类型。"""
    pass

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            var = yield
        except DemoException as e:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(var))
    # raise RuntimeError('This line should never run.')

if __name__ == '__main__':

    cor_exc = demo_exc_handling()
    cor_exc.send(None)
    print(getgeneratorstate(cor_exc))  # GEN_SUSPENDED
    cor_exc.send(1)               # -> coroutine received: 1   
    cor_exc.send(2)               # -> coroutine received: 2
    cor_exc.close()
    print(getgeneratorstate(cor_exc))  # GEN_CLOSED
```

```python
# 如果把DemoException异常传入demo_exc_handling协程，它会处理，然后继续运行
cor_exc.throw(DemoException)  # *** DemoException handled. Continuing...
print(getgeneratorstate(cor_exc))  # GEN_SUSPENDED
```
```python
# 如果传入协程的异常没有处理，协程会停止，即状态变成'GEN_CLOSED'
cor_exc.throw(ZeroDivisionError)
Traceback (most recent call last):
		...
    ZeroDivisionError
# 由于前面已经抛出异常了，所以后面的代码无法执行，只有在控制台操作才能看出状态
print(getgeneratorstate(cor_exc))  # GEN_CLOSED
```

如果不管协程如何结束都想做些清理工作，要把协程定义体中相关的代码放入try/finally块中，

```python
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
        print('-> coroutine ending, clearing something.')
```

---

#### 5. 让协程返回值

```python
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
    avg.send(None)
'''
Traceback (most recent call last):
   ...
StopIteration: Result(count=3, average=2.0)
'''
```

发送 None 会终止循环，导致协程结束，返回结果。一如既往，生成器对象会抛出StopIteration 异常。异常对象的 value 属性保存着返回的值。

何获取协程返回的值: 把 ` avg.send(None)` 用try包含。

```python
try:
    avg.send(None)
except StopIteration as e:
    print(e)
# Result(count=3, average=2.0)
```

---

#### 6. 使用yield from

yield  from 结构会在内部自动捕获 StopIteration 异常。这种处理方式与for 循环处理StopIteration 异常的方式一样：循环机制使用用户易于理解的方式处理异常。对 yield  from 结构来说，解释器不仅会捕获 StopIteration 异常，还会把 value 属性的值变成 yield  from 表达式的值。

yield from 可用于简化 for 循环中的 yield 表达式：

```python
def gen():
    for i in "ABC":
        yield i
    for j in [1, 2, 3]:
        yield j

print(list(gen()))  # ['A', 'B', 'C', 1, 2, 3]
```

使用yield from：

```python
def gen2():
    yield from "ABC"
    yield from [1, 2, 3]

print(list(gen2()))  # ['A', 'B', 'C', 1, 2, 3]
```

yield from 在扁平化处理嵌套型的序列中的应用：

```python
def gen3(*args):
    for item in args:
        yield from item

a = (1, 2, 3)
b = "ABC"
print(list(gen3(a, b)))  # [1, 2, 3, 'A', 'B', 'C']
```

`yield  from  x`  表达式对 x 对象所做的第一件事是，调用 iter(x)，从中获取迭代器，因此 x 可以是任何可迭代的对象。

如果 yield  from 结构唯一的作用是替代产出值的嵌套 for 循环，这个结构很有可能不会添加到 Python 语言中。yield  from 结构的本质作用无法通过简单的可迭代对象说明，而要发散思维，使用嵌套的生成器。

yield  from 的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连接起来，这样二者可以直接发送和产出值，还可以直接传入异常，而不用在位于中间的协程中添加大量处理异常的样板代码。有了这个结构，协程可以通过以前不可能的方式委托职责。（见《流畅的Python》）