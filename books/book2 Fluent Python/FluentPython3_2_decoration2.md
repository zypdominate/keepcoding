#### 1. 一个简单的装饰器

定义了一个装饰器，它会在每次调用被装饰的函数时计时，然后把经过的时间、传入的参数和调用的结果打印出来。

```python
# a3_4_decorate.py
import time

def clock(func):
    def clocked(*args):  # 定义内部函数 clocked
        t0 = time.perf_counter()
        res = func(*args)   # 这行代码可用，是因为 clocked 的闭包中包含自由变量 func
        elapsed = time.perf_counter() - t0
        name = func.__name__
        args_str = ', '.join(repr(arg) for arg in args)
        print(f'[{elapsed:>2.8}s], {name}({args_str})--> {res}')
        return res
    return clocked  # 返回内部函数，取代被装饰的函数。
```

```python
# a3_4_decorate_func.py
import time
from a3_4_decorate import clock

@clock
def test_sleep(seconds):
    time.sleep(seconds)

@clock
def test_factorial(n):
    return 1 if n < 2 else n * test_factorial(n-1)

if __name__ == '__main__':
    test_sleep(1.2)
    test_factorial(6)

# [1.2008935s], test_sleep(1.2)--> None
# [2e-06s], test_factorial(1)--> 1
# [0.0001048s], test_factorial(2)--> 2
# [0.0001478s], test_factorial(3)--> 6
# [0.0001863s], test_factorial(4)--> 24
# [0.0002236s], test_factorial(5)--> 120
# [0.0002705s], test_factorial(6)--> 720
```

在示例中，test_factorial 会作为 func 参数传给 clock。然后，clock 函数会返回 clocked 函数，Python 解释器在背后会把 clocked 赋值给 factorial。其实，导入 clockdeco_demo 模块后查看 factorial 的 `__name__` 属性:

```python
# a3_4_decorate_func_import.py
import a3_4_decorate_func

print(a3_4_decorate_func.test_factorial.__name__)
print(a3_4_decorate_func.test_sleep.__name__)
# clocked
# clocked
```

所以，现在 test_factorial 保存的是 clocked 函数的引用。自此之后，每次调用 test_factorial(n)，执行的都是 clocked(n)。

这是**装饰器的典型行为**：**把被装饰的函数替换成新函数，二者接受相同的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做些额外操作。**

本例中实现的 clock 装饰器有几个缺点：不支持关键字参数，而且遮盖了被装饰函数的` __name__ `和` __doc__ `属性。下面将使用 functools.wraps 装饰器把相关的属性从 func复制到 clocked 中。

```python
# a3_4_decorate_wraps.py
import time
from functools import wraps

def clock(func):
    @wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        args_list = []
        if args:
            args_list.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = [f'{k}={v}' for k, v in sorted(kwargs.items())]
            args_list.append(', '.join(pairs))
        args_str = ', '.join(args_list)
        print(f'[{elapsed:>2.8}s], {name}({args_str})--> {res}')
        return res

    return clocked
```

```python
# a3_4_decorate_wraps_run.py
import time
from a3_4_decorate_wraps import clock

@clock
def test_sleep(seconds, name=None):
    time.sleep(seconds)

@clock
def test_factorial(n, name="fi"):
    return 1 if n < 2 else n * test_factorial(n - 1)

if __name__ == '__main__':
    test_sleep(1.2, name='xiaoming')
    test_factorial(6, name='fi')

# [1.200119s], test_sleep(1.2, name=xiaoming)--> None
# [1.7e-06s], test_factorial(1)--> 1
# [6.01e-05s], test_factorial(2)--> 2
# [8.98e-05s], test_factorial(3)--> 6
# [0.0001158s], test_factorial(4)--> 24
# [0.0001468s], test_factorial(5, name=fi)--> 120
```

---

#### 2. 标准库中的装饰器

Python 内置了三个用于装饰方法的函数：property、classmethod 和 staticmethod。

另一个常见的装饰器是 **functools.wraps**，它的作用是协助构建行为良好的装饰器。

标 准 库 中 最 值 得 关 注 的 两 个 装 饰 器 是 lru_cache 和全新的singledispatch（Python 3.4 新增）。这两个装饰器都在 functools 模块中定义。

###### 2.1 使用functools.lru_cache做备忘

**functools.lru_cache** 是非常实用的装饰器，它实现了备忘（memoization）功能。这是一项优化技术，它把耗时的函数的结果保存起来，避免传入相同的参数时重复计算。LRU 三个字母是“Least Recently Used”的缩写，表明缓存不会无限制增长，一段时间不用的缓存条目会被扔掉。

生成第 *n* 个斐波纳契数这种慢速递归函数适合使用 lru_cache：

```python
from a3_4_decorate import clock

@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    print(fibonacci(6))
'''
[9e-07s], fibonacci(0)--> 0
[1.2e-06s], fibonacci(1)--> 1
[9.52e-05s], fibonacci(2)--> 1
[8e-07s], fibonacci(1)--> 1
[1e-06s], fibonacci(0)--> 0
[9e-07s], fibonacci(1)--> 1
[4.64e-05s], fibonacci(2)--> 1
[9.12e-05s], fibonacci(3)--> 2
[0.0002324s], fibonacci(4)--> 3
3
'''
```

这里生成第 *n* 个斐波纳契数，递归方式非常耗时，fibonacci(0) 调用了 2 次，fibonacci(1) 调用了 3 次……但是，

如果增加两行代码，使用 lru_cache，使用缓存实现，速度更快，性能会显著改善。

```python
from functools import lru_cache
from a3_4_decorate import clock

@lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    print(fibonacci(4))

'''
[1.6e-06s], fibonacci(0)--> 0
[2e-06s], fibonacci(1)--> 1
[0.0001693s], fibonacci(2)--> 1
[3.3e-06s], fibonacci(3)--> 2
[0.0002637s], fibonacci(4)--> 3
3
'''
```

需要注意的是：必须像常规函数那样调用 lru_cache。这一行中有一对括号：@functools.lru_cache()。这么做的原因是，lru_cache 可以接受配置参数。另外，这里叠放了装饰器：@lru_cache() 应用到 @clock 返回的函数上。

特别要注意，lru_cache 可以使用两个可选的参数来配置。它的签名是：functools.lru_cache(maxsize=128, typed=False)：maxsize 参数指定存储多少个调用的结果。缓存满了之后，旧的结果会被扔掉，腾出空间。为了得到最佳性能，maxsize 应该设为 2 的幂。typed 参数如果设为 True，把不同参数类型得到的结果分开保存，即把通常认为相等的浮点数和整数参数（如 1 和 1.0）区分开。顺便说一下，因为 lru_cache 使用字典存储结果，而且键根据调用时传入的定位参数和关键字参数创建，所以被 lru_cache 装饰的函数，它的所有参数都必须是可散列的。

---

###### 2.2 单分派泛函数

假设我们在开发一个调试 Web 应用的工具，我们想生成 HTML，显示不同类型的 Python对象。

```python
import html
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)
```

这个函数适用于任何 Python 类型，但是现在我们想做个扩展，让它使用特别的方式显示某些类型。

- str：把内部的换行符替换为` '<br>\n'`；不使用` <pre>`，而是使用` <p>`。

- int：以十进制和十六进制显示数字。

- list：输出一个 HTML 列表，根据各个元素的类型进行格式化。

因为 Python 不支持重载方法或函数，所以我们不能使用不同的签名定义 htmlize 的变体，也无法使用不同的方式处理不同的数据类型。在 Python 中，一种常见的做法是把 htmlize变成一个分派函数，使用一串 if/elif/elif，调用专门的函数，如 htmlize_str、htmlize_int，等等。这样不便于模块的用户扩展，还显得笨拙：时间一长，分派函数 htmlize 会变得很大，而且它与各个专门函数之间的耦合也很紧密。

Python 3.4 新增的 functools.singledispatch 装饰器可以把整体方案拆分成多个模块，甚至可以为你无法修改的类提供专门的函数。使用 @singledispatch 装饰的普通函数会变成泛函数（generic function）：根据第一个参数的类型，以不同方式执行相同操作的一组函数。

```python
# singledispatch 创建一个自定义的 htmlize.register 装饰器，
# 把多个函数绑在一起组成一个泛函数
from functools import singledispatch

import numbers
import html
from collections import abc

@singledispatch  # @singledispatch 标记处理 object 类型的基函数
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)

@htmlize.register(str)
def _(text):   # 专门函数的名称无关紧要；_ 是个不错的选择，简单明了。
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)

@htmlize.register(numbers.Integral)
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)

@htmlize.register(tuple)   # 可以叠放多个register装饰器，让同一个函数支持不同类型
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

print(htmlize({1, 2, 3}))  # <pre>{1, 2, 3}</pre>
print(htmlize(abs))  # <pre>&lt;built-in function abs&gt;</pre>
print(htmlize('Heimlich & Co.\n- a game'))
# <p>Heimlich &amp; Co.<br>
# - a game</p>
print(htmlize(42))  # <pre>42 (0x2a)</pre>
print(htmlize(['alpha', 66, {3, 2, 1}]))
# <ul>
# <li><p>alpha</p></li>
# <li><pre>66 (0x42)</pre></li>
# <li><pre>{1, 2, 3}</pre></li>
# </ul>
```

只要可能，注册的专门函数应该处理抽象基类（如 **numbers.Integral** 和 **abc.MutableSequence**），不要处理具体实现（如 int 和 list）。这样，代码支持的兼容类型更广泛。例如，Python扩展可以子类化numbers.Integral，使用固定的位数实现 int 类型。

**singledispatch 机制的一个显著特征是，你可以在系统的任何地方和任何模块中注册专门函数**。如果后来在新的模块中定义了新的类型，可以轻松地添加一个新的专门函数来处理那个类型。此外，你还可以为不是自己编写的或者不能修改的类添加自定义函数。

---

#### 3. 叠放装饰器

把 @d1 和 @d2 两个装饰器按顺序应用到 f 函数上，作用相当于 f = d1(d2(f))。

```python
def d1(func):
    def decorate():
        pass
    return decorate

def d2(func):
    def decorate():
        pass
    return decorate

@d1 
@d2 
def f(): 
    print('f')
 
# 等同于：
def f(): 
    print('f') 
f = d1(d2(f))
```

---

#### 4. 参数化装饰器

解析源码中的装饰器时，Python 把被装饰的函数作为第一个参数传给装饰器函数。那怎么让装饰器接受其他参数呢？答案是：**创建一个装饰器工厂函数，把参数传给它，返回一个装饰器，然后再把它应用到要装饰的函数上**。

```python
registry = set()

def register(active=True):
    def decorate(func):  # decorate 这个内部函数是真正的装饰器；它的参数是一个函数。
        print(f'running register(active={active})->decorate({func})')
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func  # decorate 是装饰器，必须返回一个函数。
    return decorate  # register 是装饰器工厂函数，因此返回 decorate。


@register(active=False)  # 为了接受参数，新的register装饰器必须作为函数调用。
def f1():
    print('running f1()')

@register()
def f2():
    print('running f2()')

def f3():
    print('running f3()')

if __name__ == '__main__':
    print(f'registry:{registry}')
    f1()
    f2()
    f3()
    print(f'registry:{registry}')
    
'''
running register(active=False)->decorate(<function f1 at 0x000001EDB675B378>)
running register(active=True)->decorate(<function f2 at 0x000001EDB675B400>)
registry:{<function f2 at 0x000001EDB675B400>}
running f1()
running f2()
running f3()
registry:{<function f2 at 0x000001EDB675B400>}
'''
```

@register 工厂函数必须作为函数调用，并且传入所需的参数。即使不传入参数，register 也必须作为函数调用（@register()），即要返回真正的装饰器 decorate。

关键是，register() 要返回 decorate，然后把它应用到被装饰的函数上。

如果不使用 @ 句法，那就要像常规函数那样使用 register；若想把 f 添加到 registry中，则装饰 f 函数的句法是 register()(f)；不想添加（或把它删除）的话，句法是register(active=False)(f)。

```python
from a3_5_decorate_parameter import register, registry, f1, f2, f3

# running register(active=False)->decorate(<function f1 at 0x000002183A36B400>)
# running register(active=True)->decorate(<function f2 at 0x000002183A36B488>)

print(registry)
# {<function f2 at 0x000002183A36B488>}

register()(f3)
# running register(active=True)->decorate(<function f3 at 0x000002183A36B378>)
print(registry)
# {<function f2 at 0x000002183A36B488>, <function f3 at 0x000002183A36B378>}

register(active=False)(f2)
# running register(active=False)->decorate(<function f2 at 0x000002183A36B488>)
print(registry)
# {<function f3 at 0x000002183A36B378>}
```

---

#### 5. 参数化clock装饰器

为clock添加一个功能：让用户传入一个格式字符串，控制被装饰函数的输出。

```python
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):  # clock 是参数化装饰器工厂函数。
    def decorate(func):			# decorate 是真正的装饰器
        def clocked(*args):		# clocked 包装被装饰的函数
            t0 = time.time()
            _res = func(*args)
            result = repr(_res)
            elapsed = time.time() - t0
            name = func.__name__
            args_str = ', '.join(repr(arg) for arg in args)
            print(fmt.format(**locals()))  # 使用 **locals() 是为了在 fmt 中引用 clocked 的局部变量
            return _res
        return clocked
    return decorate

if __name__ == '__main__':
    @clock()
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)
'''
[0.12307549s] snooze((0.123,)) -> None
[0.12305403s] snooze((0.123,)) -> None
[0.12399721s] snooze((0.123,)) -> None
'''
```

```python
    @clock('{name}: {elapsed}s')
    def snooze(seconds):
        time.sleep(seconds)
    # snooze: 0.12392497062683105s

    @clock('{name}({args}) dt={elapsed:0.3f}s')
    def snooze(seconds):
        time.sleep(seconds)
    # snooze((0.123,)) dt=0.123s
```

