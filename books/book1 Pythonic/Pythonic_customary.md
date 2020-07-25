**Rome was not built in one day， coding will not advance vigorously with one effort.**

编程语言都有其惯用法，了解掌握这些用法有助于帮助写出更加专业和精简的程序。



## 利用Assert发现问题

assert 主要是为调试使用，方便检查程序的异常和不恰当的值。

`__debug__`的值为True。

- 断言不要滥用，应该使用在正常逻辑不可到达之处、正常情况下总是为真的场合
- 能使用python的异常处理，就可以不使用断言
- 函数调用后，需要确认返回值是否合理时可以使用断言
- 当条件是业务逻辑继续下去的先决条件时可以使用断言



## 数据值交换不推荐使用中间变量

```python
import dis
def swap1():
    a = 1
    b = 2
    a, b = b, a
    
>>>dis.dis(swap1)
  2           0 LOAD_CONST               1 (1)
              2 STORE_FAST               0 (a)
  3           4 LOAD_CONST               2 (2)
              6 STORE_FAST               1 (b)
  4           8 LOAD_FAST                1 (b)
             10 LOAD_FAST                0 (a)
             12 ROT_TWO
             14 STORE_FAST               0 (a)
             16 STORE_FAST               1 (b)
             18 LOAD_CONST               0 (None)
             20 RETURN_VALUE
```

```python
def swap2():
    a = 11
    b = 22
    temp = a
    a = b
    b = temp
    
>>>dis.dis(swap2)
  2           0 LOAD_CONST               1 (11)
              2 STORE_FAST               0 (a)
  3           4 LOAD_CONST               2 (22)
              6 STORE_FAST               1 (b)
  4           8 LOAD_FAST                0 (a)
             10 STORE_FAST               2 (temp)
  5          12 LOAD_FAST                1 (b)
             14 STORE_FAST               0 (a)
  6          16 LOAD_FAST                2 (temp)
             18 STORE_FAST               1 (b)
             20 LOAD_CONST               0 (None)
             22 RETURN_VALUE
```

Python中的字节码是一种类似汇编指令的中间语言，但是一个字节码指令并不是对应一个机器指令。

swap1中的`a, b = b, a`对应着代码块的12-16行（2个LOAD_FAST, 2个STORE_FAST, 1个ROT_TWO），而swap2中第4-6行对应着13-18行（3个LOAD_FAST，3个STORE_FAST），ROT_TWO的主要作用是交换两个栈的最顶层元素，它比执行一个LOAD_FAST+STORE_FAST快。



## 充分利用Lazy evaluation特性

- 避免不必要的计算，带来性能上的提升
  - 条件表达式，如if x and y， 在x为False情况，或者if x or y，在x为True的情况下，y都是不计算的
  - 对于and条件表达式，应该将值为False可能性高的变量写前面；对于or条件表达式，将值为True可能性高的写前面

- 节省空间，使得无限循环的数据结构变成可能

  - 生成器表达式：每次需要计算时才通过yield产生所需要的元素

  ```python
  def fib():
  	a, b = 0, 1
    while True:
      yield a
      a, b = b, a+b
  ```

  

## 不推荐使用type来检查类型

作为动态语言的强类型脚本语言，Python中的变量在定义时并不会指明具体的类型，Python解释器在运行时自动进行类型检查并根据需要进行隐式类型转换， 在出错时通过抛出异常来处理。

```python
class UserInt(int):  # 继承int
    def __init__(self, var=0):
        # self._var = int(var)
        super(UserInt, self).__init__()
        self._var = int(var)

    def __add__(self, other):
        if isinstance(other, UserInt):
            return UserInt(self._var + other._var)
        return self._var + other

    def __iadd__(self, other):
        raise NotImplementedError("not support operation")

    def __str__(self):
        return str(self._var)

    def __repr__(self):
        return f"Interger {self._var}"


user1 = UserInt()
user2 = UserInt(2)
user3 = UserInt('3')
print(user1, user2, user3)  # 0 2 3
print(user1 + user2)  # 2
print(user3 + 12)  # 15

type_user1 = type(user1)  # <class '__main__.UserInt'>
type_int = type(int)  # <class 'type'>
if type_user1 is type_int: # False
    print(True)
else:
    print(False)
    
print(UserInt, type(UserInt))  # <class '__main__.UserInt'> <class 'type'>
print(UserInt(), type(UserInt()))  # 0 <class '__main__.UserInt'>
print(user1, type(user1))  # 0 <class '__main__.UserInt'>
print(int, type(int))  # <class 'int'> <class 'type'>
```

虽然UserInt继承于int，但是type()并不认为user1是int类型，显然是不合理的。**基于内建类型扩展的用户定义类型，type函数并不能准确的返回结果。**

推荐使用 isinstance()函数:

```python
if isinstance(user1, type(UserInt())):  # True
    print(True)
else:
    print(False)

if isinstance(user1, int):  # True
    print(True)
else:
    print(False)
```



## 使用enumerate()获取序列的索引和值

小需求：对某一序列进行迭代并获取序列中的元素进行处理

```python
for i, ele in enumerate(list_):
    print(f"i:{i}, element:{ele}")

# 推荐 enumerate(sequence,start=0)
# sequence可以是任何可迭代对象，函数返回本质上是一个迭代器，可用next()获取下一个迭代元素
enu = enumerate(list_)
next(enu)  # (0, 1)

# enumerate内部实现原理
def mock_enumerate(sequence, start=0):
    n = start
    for ele in sequence:
        yield n, ele
        n += 1

# 实现自己的enumerate()函数:反序列
def reverse_enumerate(sequence, start=0):
    n = -1
    for ele in reversed(sequence):
        yield len(sequence)+n, ele
        n -= 1

# 对于字典的迭代，enumerate()并不适合，而是应该使用方法items()
mydict = {1:'aa',2:'bb'}
for key,value in mydict.items():
```



## is 和 == 的适用场景

两个对象相等应该用 == 

| 操作符 | 意义            |
| ------ | --------------- |
| is     | object identity |
| ==     | equal           |

is的作用是用来检验对象的标识符是否一致，也就是比较两个对象在内存中是否拥有同一块内存空间，它并不适合用来判断两个字符串是否相等。x is y 仅当x和y是同一个对象的时候才返回True，基本相当于id(x) = id(y)。而==是用来检验两个对象的值是否相等的，调用的是内部的`__eq__`方法， `a == b`相当于 `a.__eq__(b)` ，` == `是可以被重载的，而is不能被重载。

另外Python中的string interning（**字符串驻留**）机制得处理较小的字符串和较长字符串有所不同。对于较小的字符串，为了提高系统性能会保留其值的一个副本，当创建新的字符串时直接指向该副本即可。所以有时有的对象有着相同的内容，但是标识符却不相同，用==判断为True，用is判断为False。

```python
short_a = 'aa'
short_b = 'aa'
id(short_a), id(short_b)
Out[1: (2899755577672, 2899755577672)

short_a == short_b
Out[3]: True
short_a is short_b
Out[5]: True
    
    
long_b = "just test long string"
long_a = "just test long string"
id(long_a), id(long_b)
Out[2]: (2899904998112, 2899906473896)
  
long_a == long_b
Out[4]: True
  
long_a is long_b
Out[6]: False
```

