## 上下文管理器

#### 1. 上下文管理器和with块

**上下文管理器对象存在的目的是管理 with 语句，就像迭代器的存在是为了管理 for 语句一样。**

with 语句的目的是简化 try/finally 模式。这种模式用于保证一段代码运行完毕后执行某项操作，即便那段代码由于异常、return 语句或 sys.exit() 调用而中止，也会执行指定的操作。finally 子句中的代码通常用于释放重要的资源，或者还原临时变更的状态。

上下文管理器协议包含 `__enter__` 和 `__exit__` 两个方法。with 语句开始运行时，会在上下文管理器对象上调用 `__enter__` 方法。with 语句运行结束后，会在上下文管理器对象上调用 `__exit__ ` 方法，以此扮演 finally 子句的角色。

with 语句会设置一个临时的上下文，交给上下文管理器对象控制，并且负责清理上下文。这么做能避免错误并减少样板代码，因此 API 更安全，而且更易于使用。除了自动关闭文件之外，with 块还有很多用途。

最常见的例子是确保关闭文件对象：

```python
with open("a5_3_with.py") as f:
    content = f.read(100)

print(f)  # fp 变量仍然可用
# <_io.TextIOWrapper name='a5_3_with.py' mode='r' encoding='cp936'>
print(len(content))  
# 100
print(f.closed, f.encoding)
# True cp936

# f.read(10)  
# ValueError: I/O operation on closed file.
# 不能在 fp 上执行 I/O 操作，因为在 with 块的末尾，调用TextIOWrapper.__exit__方法把文件关闭了。
```

执行 with 后面的表达式得到的结果是上下文管理器对象，不过，把值绑定到目标变量上（as 子句）是在上下文管理器对象上调用 `__enter__` 方法的结果。

不管控制流程以哪种方式退出 with 块，都会在上下文管理器对象上调用 `__exit__` 方法，而不是在 `__enter__` 方法返回的对象上调用。

with 语句的 as 子句是可选的。对 open 函数来说，必须加上 as 子句，以便获取文件的引用。不过，有些上下文管理器会返回 None，因为没什么有用的对象能提供给用户。



上下文管理器与 `__enter__` 方法返回的对象之间的区别：

```python
class LookingGlass():
    def __enter__(self):  # ❶
        import sys
        self.origin_write = sys.stdout.write  # ❷
        sys.stdout.write = self.reverse_write  # ❸
        return "reversed word -> drow desrever"  # ❹

    def reverse_write(self, context):  # ❺
        self.origin_write(context[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb): # ❻
        import sys  # ❼
        sys.stdout.write = self.origin_write  # ❽
        if exc_type is ZeroDivisionError:  # ❾
            print("do not divide by zero")
            return True  # ❿
        # ⓫

with LookingGlass() as look:
    print("I'm looking sth.")
    print(look)
    
# .hts gnikool m'I
# reversed word>-drow desrever
```

1. ❶除了self之外，Python调用`__enter__`方法时不传入其他参数。
2. ❷ 把原来的sys.stdout.write方法保存在一个实例属性中，供后面使用。
3. ❸ 为sys.stdout.write打猴子补丁，替换成自己编写的方法。
4. ❹ 返回'reversed word -> drow desrever'字符串，这样才有内容存入目标变量look。
5. ❺ 这是用于取代sys.stdout.write的方法，把text参数的内容反转，然后调用原来的实现。
6. ❻ 如果一切正常，Python调用`__exit__`方法时传入的参数是None, None, None；如果抛出了异常，这三个参数是异常数据，如下所述。
7. ❼ 重复导入模块不会消耗很多资源，因为Python会缓存导入的模块。
8. ❽ 还原成原来的sys.stdout.write方法。
9. ❾ 如果有异常，而且是ZeroDivisionError类型，打印一个消息……
10. ❿ ……然后返回True，告诉解释器，异常已经处理了。
11. ⓫ 如果 `__exit__` 方法返回None，或者True之外的值，with块中的任何异常都会向上冒泡。

传给 `__exit__` 方法的三个参数列举如下。

- exc_type：异常类（例如 ZeroDivisionError）；

- exc_value：异常实例，有时会有参数传给异常构造方法，例如错误消息，这些参数可以使用 exc_value.args 获取；

- exc_tb：traceback 对象；

  

在 with 块之外使用 LookingGlass 类：

```python
manager = LookingGlass()
print(manager)
content = manager.__enter__()
print("12345")
print(manager)
print(content)

'''
<__main__.LookingGlass object at 0x0000019F7625D828>
54321
>828D5267F9100000x0 ta tcejbo ssalGgnikooL.__niam__<
reversed word >- drow desrever
'''
```

---

#### 2. contextlib模块中的实用工具

@contextmanager 装饰器能减少创建上下文管理器的样板代码量，因为不用编写一个完整的类，定义 `__enter__` 和 `__exit__` 方法，而只需实现有一个 yield 语句的生成器，生成想让`__enter__` 方法返回的值。

在使用 @contextmanager 装饰的生成器中，yield 语句的作用是把函数的定义体分成两部分：**yield 语句前面的所有代码在 with 块开始时（即解释器调用 `__enter__` 方法时）执行，yield 语句后面的代码在 with 块结束时（即调用 `__exit__` 方法时）执行**。

```python
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
        # 这里是恢复成原来的 sys.stdout.write 方法。
        sys.stdout.write = oringin_write
        if msg:
            print(msg)

with lookingmirror() as l:
    print(l)
    print("12345")
    
# cnuf rorrimgnikool
# 54321
```

其中，如果在 with 块中抛出了异常，Python 解释器会将其捕获，然后在 lookingmirror 函数的 yield 表达式里再次抛出。但是，如果那里没有处理错误的代码，lookingmirror 函数会中止，永远无法恢复成原来的 sys.stdout.write 方法，导致系统处于无效状态，所以使用try来处理异常。

**使用 @contextmanager 装饰器时，要把 yield 语句放在 try/finally 语句中（或者放在 with 语句中），这是无法避免的，因为我们永远不知道上下文管理器的用户会在 with 块中做什么。**

contextlib.contextmanager 装饰器会把函数包装成实现 `__enter__` 和 `__exit__` 方法的类，通过debug可以进入源码看到类 `_GeneratorContextManager` 。

---

#### 3. if语句之外的else块

（这和上下文管理器完全没有关系，只是放此处）

else 子句不仅能在 if 语句中使用，还能在 for、while 和 try 语句中使用。for/else、while/else 和 try/else 的语义关系紧密，不过与 if/else 差别很大。

- **for**
  仅当 for 循环运行完毕时（即 **for 循环没有被 break 语句中止**，我想这也是for-else存在的意义的吧，不然就不需要else了）才运行 else 块。

- **while**
  仅当 while 循环因为条件为假值而退出时（即 **while 循环没有被 break 语句中止**）才运行 else块。

- **try**
  **仅 当 try 块 中 没 有 异 常 抛 出 时 才 运 行 else 块**。 [官方文档](https://docs.python.org/3/reference/compound_stmts.html)还指出：“else 子句抛出的异常不会由前面的 except 子句处理。”

**在所有情况下，如果异常、return、break 或 continue 语句导致控制权跳到了复合语句的主块之外，else 子句也会被跳过。**

在这些语句中使用 else 子句通常能让代码更易于阅读，而且能省去一些麻烦，不用设置控制标志或者添加额外的 if 语句。在循环中使用 else 子句的方式如下述代码片段所示：

```python
for item in my_list: 
    if item.flavor == 'banana': 
        break 
else:  # my_list中没有'banana'则抛出异常
    raise ValueError('No banana flavor found!')
```

在 try/except 块中使用 else 子句，在下述代码片段中，只有 dangerous_call() 不抛出异常，after_call() 才会执行：

```python
try:
    dangerous_call()
    after_call()
except OSError:
    print("log:OSError")
```

after_call() 不应该放在 try 块中。为了清晰和准确，try 块中应该只抛出预期异常的语句。因此，像下面这样写更好，try 块防守的是 dangerous_call() 可能出现的错误，而不是 after_call()，而且很明显，只有 try 块不抛出异常，才会执行 after_call()。

```python
try:
    dangerous_call()
except OSError:
    print("log:OSError")
else:
  	after_call()
```

