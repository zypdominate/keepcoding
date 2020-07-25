## 把函数视作对象

#### 1. 一等函数

Python 中，函数是一等对象。编程语言理论家把“一等对象”定义为满足下述条件的程序实体： 

- 在运行时创建
- 能赋值给变量或数据结构中的元素 
- 能作为参数传给函数 
- 能作为函数的返回结果

在 Python 中，整数、字符串和字典都是一等对象。函数也可以作为一等对象。

```python
def factorial(n):
    """
    阶乘
    :param n: num 
    :return: num!
    """
    return 1 if n < 1 else n * factorial(n-1)
  
factorial.__doc__
Out[2]: '\n    阶乘\n    :param n: num \n    :return: num!\n    '
factorial(30)
Out[3]: 265252859812191058636308480000000
type(factorial)
Out[4]: function
```

这是一个控制台会话，`def factorial(n):`是在“运行时”创建一个函数。`__doc__` 是函数对象众多属性中的一个。  factorial 是 function 类的实例。

函数对象的“一等”本性:
我们可以把 factorial 函数赋值给变量 fact，然后通过变量名调用。我们还能把它作为参数传给 map 函数。map 函数返回一个可迭代对象，里面的元素是把第一个参数（一个函数）应用到第二个参数（一个可迭代对象，这里 是 range(11)）中各个元素上得到的结果。

```python
# 通过别的名称使用函数，再把函数作为参数传递
fact = factorial
fact(5)
Out[5]: 120
type(fact)
Out[6]: function
  
map(fact, range(5))
Out[7]: <map at 0x212ba2663c8>
list(map(fact, range(5)))
Out[8]: [1, 1, 2, 6, 24]
```

有了一等函数，就可以使用函数式风格编程。函数式编程的特点之一是使用高阶函数。

---

#### 2. 高阶函数

接受函数为参数，或者把函数作为结果返回的函数是高阶函数（higher-order function）。在函数式编程范式中，最为人熟知的高阶函数有 map、filter、reduce。

此外，内置函数 sorted 也是：可选的 key 参数用于提供一个函数，它会应用到各个元素上进行排序。

```python
def reverse(word): 
    return word[::-1] 
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
sorted(fruits, key=reverse)
Out[16]: ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
```

map、filter和reduce的现代替代品：

map 和 filter 还是内置函数，但是由于引入了**列表推导和生成器表达式**，它们变得没那么重要了。列表推导或生成器表达式具有 map 和 filter 两个函数的功能，而且更易于阅读。

```python
# Python3 中，map 和 filter 返回生成器（一种迭代器），因此现在它们的直接替代品是生成器表达式
list(map(fact,range(6)))
Out[17]: [1, 1, 2, 6, 24, 120]
[fact(n) for n in range(6)]   # 使用列表推导执行相同的操作。
Out[18]: [1, 1, 2, 6, 24, 120]
  
list(map(fact, filter(lambda n:n%2, range(6))))
Out[19]: [1, 6, 120]
[fact(n) for n in range(6) if n%2]  # 列表推导式，取代map、filter，并避免了lambda 表达式
Out[20]: [1, 6, 120]
```

```python
# 在 Python2中，reduce 是内置函数，但是在 Python3 中放到 functools 模块里了。
# 这个函数最常用于求和，自2003年发布的 Python2.3开始，最好使用内置的sum函数。
# 在可读性和性能方面，这是一项重大改善.
from functools import reduce
from operator import add
reduce(add, range(6))
Out[25]: 15
```

sum 和 reduce 的通用思想是把某个操作连续应用到序列的元素上，累计之前的结果，把一系列值归约成一个值。all 和 any 也是内置的归约函数。

all(iterable):  如果 iterable 的每个元素都是真值，返回 True；all([]) 返回 True。 有0即为假

any(iterable) : 只要 iterable 中有元素是真值，就返回 True；any([]) 返回 False。 有1即为真

```python
Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> all([1,0])
False
>>> all([1])
True
>>> all([])
True
>>> any([1,0])
True
>>> any([0])
False
>>> any([])
False
```

---

#### 3. 可调用对象

除了用户定义的函数，调用运算符（即 ()）还可以应用到其他对象上。如果想判断对象能否调用，可以使用内置的 callable() 函数。Python 数据模型文档列出了 **7 种可调用对象**。

1. **用户定义的函数** 

   使用 def 语句或 lambda 表达式创建。

2. **内置函数**

   使用 C 语言（CPython）实现的函数，如 len 或 time.strftime。

3. **内置方法** 

   使用 C 语言实现的方法，如 dict.get。

4. **方法** 

   在类的定义体中定义的函数。 

5. **类** 

   调用类时会运行类的 `__new__ `方法创建一个实例，然后运行` __init__ `方法，初始化实例，最后把实例返回给调用方。因为 Python 没有 new 运算符，所以调用类相当于调用函数。（通常，调用类会创建那个类的实例，不过覆盖 `__new__ `方法的话，也可能出现 其他行为。）

6. **类的实例** 

   如果类定义了` __call__ `方法，那么它的实例可以作为函数调用。

7. **生成器函数** 

   使用 yield 关键字的函数或方法。调用生成器函数返回的是生成器对象。

   

Python 中有各种各样可调用的类型，因此判断对象能否调用，最安全的方法是使用内置的 callable() 函数： 

```python
>>> [callable(item) for item in [str, abs, 100]]
[True, True, False]
```



#### 4. 用户可调用的类型

不仅 Python 函数是真正的对象，任何 Python 对象都可以表现得像函数。为此，只需实现实例方法 `__call__`。

```python
import random

class BingoCase(object):
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pickitem(self):
        try:
            return self._items.pop()
        except IndexError as e:
            raise LookupError('pick from empty BingoCase')

    def __call__(self, *args, **kwargs):  # bingo.pickitem()的快捷方式为bingo()
        return self.pickitem()


bingo = BingoCase([1, 2, 3, 3, 4, 5])
print(bingo.pickitem())
print(bingo())
print(callable(bingo))
```

实现` __call__ `方法的类是创建函数类对象的简便方式，此时必须在内部维护一个状态，让它在调用之间可用，例如 BingoCage 中的剩余元素。装饰器就是这样，有时要在多次调用之间“记住”某些事（例如备忘memoization），即缓存消耗大的计算结果，供后面使用。

创建保有内部状态的函数，还有一种截然不同的方式——闭包。

---

#### 5. 函数注解

Python3提供了一种句法，用于为函数声明中的参数和返回值附加元数据。

```python
def clip(text: str, max_len: 'int > 0' = 8) -> str:  # 有注解的函数声明
    """
    在max_len前面或后面的第一个空格处截断文本
    """
    end = None
    space_before = space_after = ''
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        print(space_before)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            print(space_after)
            if space_after >= 0:
                end = space_after
    if end is None:  # 没找到空格
        end = len(text)
    return text[:end].rstrip()

print(clip("1adsfd2sdfjkl 3dsfa 4jskldf"))
print(clip.__annotations__)
'''
1adsfd2sdfjkl 3dsfa
{'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}
'''
```

函数声明中的各个参数可以**在 : 之后增加注解表达式**。如果**参数有默认值，注解放在参数名和 = 号之间**。如果想**注解返回值，在 ) 和函数声明末尾的 : 之间添加 -> 和一个表达式**。那个表达式可以是任何类型。注解中最常用的类型是类（如 str 或 int）和字符串（如'int > 0'）。在示例中，max_len 参数的注解用的是字符串。

注解不会做任何处理，只是存储在函数的 `__annotations__ `属性（一个字典）中。

Python 对注解所做的唯一的事情是，把它们存储在函数的` __annotations`__ 属性里。仅此而已，Python 不做检查、不做强制、不做验证，什么操作都不做。换句话说，注解对Python 解释器没有任何意义。注解只是元数据，可以供 IDE、框架和装饰器等工具使用。

---

#### 6. 支持函数式编程的包

**operator模块**

operator 模块为多个算术运算符提供了对应的函数，从而避免编写 lambda a, b: a*b 这种平凡的匿名函数。

```python
from functools import reduce
def func(n):	
    return reduce(lambda a, b:a*b, range(1,n+1))
func(4)
Out[2]: 24
  
from operator import mul
def fact(n):
    return reduce(mul, range(1,n+1))
fact(4)
Out[3]: 24
```

operator 模块中还有一类函数，能替代从序列中取出元素或读取对象属性的 lambda 表达式：因此，itemgetter 和 attrgetter 其实会自行构建函数。

**itemgetter** 使用 [] 运算符，因此它不仅支持序列，还支持映射和任何实现 `__getitem__` 方法的类。itemgetter 的常见用途：根据元组的某个字段给元组列表排序

```python
metro_data = [ 
  ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)), 
  ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)), 
  ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)), 
  ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)), 
  ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)), ]

from operator import itemgetter
for city in sorted(metro_data, key=itemgetter(1)):
    print(city)
    
# 如果把多个参数传给 itemgetter，它构建的函数会返回提取的值构成的元组：
names = itemgetter(0, 1)
for city in metro_data:
    print(names(city))
"""
('Tokyo', 'JP')
('Delhi NCR', 'IN')
('Mexico City', 'MX')
('New York-Newark', 'US')
('Sao Paulo', 'BR')
"""
```

**attrgetter** 与 itemgetter 作用类似，它创建的函数根据名称提取对象的属性。如果把多个属性名传给 attrgetter，它也会返回提取的值构成的元组。此外，如果参数名中包含 .（点号），attrgetter 会深入嵌套对象，获取指定的属性。这些行为如下例所示，这个控制台会话不短，因为我们要构建一个嵌套结构，这样才能展示attrgetter 如何处理包含点号的属性名。

```python
from collections import namedtuple 

metro_data = [ 
('Tokyo', 'JP', 36.933, (35.689722, 139.691667)), 
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)), 
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)), 
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)), 
('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)), ]

LatLong = namedtuple('LatLong', 'lat long') 
Metropolis = namedtuple('Metropolis', 'name cc pop coord') 
metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) for name, cc, pop, (lat, long) in metro_data]

metro_areas[0]
Out[3]: Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722, long=139.691667))
metro_areas[0].coord.lat
Out[4]: 35.689722
  
from operator import attrgetter
name_lat = attrgetter('name', 'coord.lat')  # 定义一个 attrgetter，获取 name 属性和嵌套的 coord.lat 属性
for city in sorted(metro_areas, key=attrgetter('coord.lat')): # 使用 attrgetter，按照纬度排序城市列表。
    print(name_lat(city)) 
    
('Sao Paulo', -23.547778)
('Mexico City', 19.433333)
('Delhi NCR', 28.613889)
('Tokyo', 35.689722)
('New York-Newark', 40.808611)
```

 operator 模块中定义的部分函数（省略了以 _ 开头的名称，因为它们基本上是实现细节）:

```python
[name for name in dir(operator) if not name.startswith('_')] 
['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains', 'countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt', 'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imatmul', 'imod', 'imul', 'index', 'indexOf', 'inv', 'invert', 'ior', 'ipow', 'irshift', 'is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le', 'length_hint', 'lshift', 'lt', 'matmul', 'methodcaller', 'mod', 'mul', 'ne', 'neg', 'not_', 'or_', 'pos', 'pow', 'rshift', 'setitem', 'sub', 'truediv', 'truth', 'xor']
```

**methodcaller** 它的作用与 attrgetter和 itemgetter 类似，它会自行创建函数。methodcaller 创建的函数会在对象上调用参数指定的方法。

```python
from operator import methodcaller

s = "abcd efg"
upcase = methodcaller('upper')
upcase(s)
Out[16]: 'ABCD EFG'
  
replace_case = methodcaller('replace',' ','-')
replace_case(s)
Out[18]: 'abcd-efg'
```

