**Rome was not built in one day， coding will not advance vigorously with one effort.**

# 内部机制

## Python对象协议

可以这样比方：在Python中我需要调用你的某个方法，你正好有这个方法。

举例：如果有占位符%s，那么按照字符串转换的协议，Python会自动去调用相应对象的`__str__()`方法。

```python
class Obj(object):
    def __str__(self):
        return 'called __str__' 
    
obj = Obj()
print(obj)  # called __str__
```

除了`__str__()`方法，其他`__repr__()`、`__init__`、`__floate__`、`__nonezero__`等，统称为类型转换协议。

其他协议：

1. 用于比较大小的协议
   `__cmp__()`方法：当两者相等时返回0，当self<other时返回负值，反之返回正值。Python又有`__eq__()`、`__lt__()`、`__gt__()`等来实现相等、不等、小于和大于的判定，这就是Python对==、!=、<、>等操作符的进行重载的支撑机制。
2. 数值类型相关的协议
   - 数值运算符：`__add__`、`__sub__`、`__mul__`、`__div__`、`__pow__`
   - 位运算符：`__lshift__`、`__rshift__`、`__and__`、`__or__`、`__xor__`、`__invert__`
   - 运算赋值符：`__iadd__`、`__isub__`、`__imul__`、`__idiv__`、`__ipow__`
   - 其他：`__pos__` - 正、`__neg__` - 负、`__abs__` - 绝对值

3. 容器类型协议

   - python中内置了len函数，通过`__len__`完成

   - `__getitem__`、`__setitem__`、`__delitem__`对应读、写和删除
   - `__reversed__`对内置函数reversed支持
   - 对成员关系的判断符in和not in的支持：`__contained__`

4. 可调用对象协议
   可调用对象即类似函数对象，能够让类实例表现得像函数一样，这样就可以让每一个函数调用都有所不同。

   ```python
   class Functor(object):
       def __init__(self, content):
           self._content = content
   
       def __call__(self, *args, **kwargs):
           print(f'do something {self._content}')
   
   func = Functor("a1")
   func2 = Functor("a2")
   
   func()   # do something a1
   func2()	 # do something a2
   ```

5. 与可调用对象差不多的，还有一个可哈希对象，它是用过`__hash__()`方法来支持hash()这个内置函数的，在创建自己的类型时非常有用，因为只有支持可哈希协议的类型才能作为dict的键类型（不过只要继承自object的新式类默认就支持了）。

6. 上下文管理器协议，也就是对with语句的支持。协议通过`__enter__`、`__exit__`两个方法来实现对资源的清理，确保资源无论在什么情况下都会被正常清理。



## 迭代器协议

- 实现了一个`__iter__()`方法，返回一个迭代器

- 实现next()方法，返回当前元素，并指向下一个元素的位置，如果当前元素已无元素，则抛出StopIteration异常。

```python
mylist = range(2)
next(mylist)
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-10-bae65c1f3ff5>", line 1, in <module>
    next(mylist)
TypeError: 'range' object is not an iterator
  
myiter = mylist.__iter__()
myiter
Out[2]: <range_iterator at 0x208ddf3b3f0>
next(myiter)
Out[3]: 0
next(myiter)
Out[4]: 1
next(myiter)
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-15-ce4a7df7b15f>", line 1, in <module>
    next(myiter)
StopIteration
```

其实for语句就是福获取容器的迭代器、调用迭代器的next()方法以及对StopIteration进行处理等流程进行封装的语法糖（类似的还有in、not in)。

```python
mylist = range(3)
myiter = iter(mylist)

while True:
    try:
        print(next(myiter))
    except StopIteration:
        break
```

使用容器的优点：

```python
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):  # 使得'Fib' object is iterable
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a

for i, j in enumerate(Fib()):
    print(j)
    if i > 10:
        break
        
# 传统使用容器储存数列
def traditional(n):
    reslist = []
    a, b = 0, 1
    count = 0
    while count < n:
        reslist.append(b)
        a, b = b, a + b
        count += 1
    return reslist

print(traditional(10))
```

**与直接使用容器的代码相比，它仅使用两个变量，显而易见更省内存，并在一些应用场合更省CPU计算资源，所以在编写代码中应当多多使用迭代器协议，避免劣化代码。**



## 生成器

如果一个函数使用了yield语句，那么它就是一个生成器函数。

当调用生成器函数时，返回一个迭代器，不过迭代器是以生成器对象的形式出现的。

```python
def fib(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield b
        a, b = b, a + b
        count += 1

print(list(fib(5)))
print(dir(fib(5)))
# ['__class__', '__del__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__name__', '__ne__', '__new__', '__next__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'gi_code', 'gi_frame', 'gi_running', 'gi_yieldfrom', 'send', 'throw']
```

相对传统使用容器储存数列，使用yield代码量减少。

通过dir(fib(5))对象带有`__iter__`和`__next__`方法可以看出它是一个迭代器。

```python
def echo(value):
    print("**begin")
    while True:
        try:
            value = yield value
        except Exception as e:
            print(e)
        finally:
            print("finish**")

gen = echo(1)
print(next(gen))  # print(gen.__next__())
print(next(gen))
print(gen.send(2))
```

```
**begin
1
finish**
None
finish**
2
finish**
```



## 基于生成器的协程

先看基于生产者消费者模型，对抢占式多线程编程实现和协程编程实现进行对比。

伪代码：

```shell
# 队列容器
var q:= new queue

# 消费者线程
loop 
	lock(q)
	get item from q
	unlock(q)
	if item
		use this item
	else
		sleep

# 消费者线程
loop
	create some new item
	lock(q)
	add the items to q
	unlock(q)
```

可以看出，线程实现至少有两点缺点：

- 对队列的操作需要有显式\隐式（使用线程安全点的队列）的加锁操作
- 消费者线程还要通过sleep把CPU资源实时地“谦让”给生产者线程使用，其中适时多久，基本上只能静态地使用经验值，效果往往不尽人意

而使用协程可以解决这个问题，以下是基于协程的生产者消费模型实现（伪代码）：

```python
# 队列容器
var q:= new queue

# 生产者协程
loop 
	while q is not full:
		create some new items
		add the items to q
	yield to consume
	
# 消费者协程
loop 
	while q is not empty
		remove some items from q
		use the items
	yield to produce
```



## 对象的管理与垃圾回收

Python并不需要用户自己来像C语言一样来管理内存，它具备垃圾回收机制。

Python中内存管理方式：使用引用计数器（Reference counting）的方法来表示该对象当前有多少个引用。当其他对象引用该对象时，其引用计数会增加1，而删除一个对当前对象的引用，其引用计数会减1。只有当引用计数的值为0时该对象才会被垃圾收集器回收，因为它表示这个对象不再被其他对象引用，是个不可达对象。

但是，其缺点是无法解决循环引用的问题，即两个对象相互引用。

