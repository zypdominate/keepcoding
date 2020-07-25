## 序列的修改、散列和切片

#### 1. 使用reprlib.repr()的序列

为了编写 Vector(3,  4)和 Vector(3,  4,  5) 这样的代码，我们可以让` __init__ `方法接受任意个参数（通过 *args）；但是，序列类型的构造方法最好接受可迭代的对象为参数，因为所有内置的序列类型都是这样做的。

如果 Vector 实例的分量超过 6 个，repr() 生成的字符串就会使用 ... 省略一部分。包含大量元素的集合类型一定要这么做，因为字符串表示形式是用于调试的（因此不想让大型对象在控制台或日志中输出几千行内容）。使用 reprlib 模块可以生成长度有限的表示形式。

```python
import math
import reprlib
from array import array


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._classname = type(self).__name__
        self._components = array(self.typecode, components)  # array('d', [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

    def __iter__(self):		# 为了迭代
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)  # 获取有限长度表示
        # "array('d', [1.0, 2.0, 3.0, 4.0, 5.0, ...])"
        components = components[components.find('['):-1]
        return f'{self._classname}({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))
      	# 这里不能像abs和bool函数里写的那样直接写self，会导致循环调用__bytes__

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])  # d b'd\x00\x00\x00\x0.....
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


vector = Vector([1, 2, 3, 4, 5, 6, 7, 8])
print(vector)  # (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
print(repr(vector))		# Vector([1.0, 2.0, 3.0, 4.0, 5.0, ...])
print(bytes(vector))
# b'd\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@\x00\x00\x00\x00\x00\x00\x14@\x00\x00\x00\x00\x00\x00\x18@\x00\x00\x00\x00\x00\x00\x1c@\x00\x00\x00\x00\x00\x00 @'
print(vector.frombytes(bytes(vector)))  # (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
```

`reprlib.repr` 这个函数用于生成大型结构或递归结构的安全表示形式，它会限制输出字符串的长度，用 '...' 表示截断的部分。希望 Vector 实例的表示形式是 Vector([3.0,  4.0,  5.0]) 这样，而不是 Vector(array('d',  [3.0,  4.0, 5.0]))，因为 Vector 实例中的数组是实现细节。

写` __repr__ `方法时，本可以生成简化的 components 显示形式 `reprlib.repr(list(self._components))`，然而，这么做有点浪费，因为要把 `self._components ` 中的每个元素复制到一个列表中，然后使用列表的表示形式。而是直接把 ` self._components ` 传给 `reprlib.repr` 函数，然后去掉 [] 外面的字符，

**调用 `repr()` 函数的目的是调试，因此绝对不能抛出异常。如果 ` __repr__ ` 方法的实现有问题，那么必须处理，尽量输出有用的内容，让用户能够识别目标对象。**

---

#### 2. 协议和鸭子模型

在 Python 中创建功能完善的序列类型无需使用继承，只需实现符合**序列协议的方法**。

在面向对象编程中，**协议是非正式的接口**，只在文档中定义，在代码中不定义。例如，Python 的序列协议只需要 `__len__`和 `__getitem__` 两个方法。任何类（如 Spam），只要使用标准的签名和语义实现了这两个方法能用在任何期待序列的地方。Spam 是不是哪个类的子类无关紧要，只要提供了所需的方法即可。

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FranchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamends clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit)
                       for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

f = FranchDeck()
for i in f:
    print(i)
print(len(f))
```

 FrenchDeck 类能充分利用 Python 的很多功能，因为它实现了序列协议，不过代码中并没有声明这一点。我们说它是序列，因为它的行为像序列，这才是重点。

不要检查它是不是鸭子、它的叫声像不像鸭子、它的走路姿势像不像鸭子，等等。具体检查什么取决于你想使用语言的**哪些行为**。 ——  Alex Martelli 

协议是非正式的，没有强制力，因此如果你知道类的具体使用场景，通常只需要实现一个协议的部分。例如，为了支持迭代，只需实现 `__getitem__` 方法，没必要提供 `__len__` 方法。

---

#### 3. 可切片的序列

让 Vector 表现为序列所需的两个方法：`__len__` 和 `__getitem__` 。

```python
class Vector:
    typecode = 'd'
    # 省略其他函数，加入len、getitem
		def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        return self._components[index]

vector = Vector(range(7))

print(len(vector))  # 7
print(vector[0])  # 0.0
print(vector[1:3])  # array('d', [1.0, 2.0])  
```

这里切片生成还只是普通的数组。

---

#### 4. 切片原理

举例：

```python
class Myseq:
    def __getitem__(self, index):
        return index
seq = Myseq()

seq[1]
1
seq[1:4]
slice(1, 4, None)

seq[1:4:2]
slice(1, 4, 2)

seq[1:4:2, 9]
(slice(1, 4, 2), 9)  # 如果[]中有逗号，那么__getitem__收到的是元组。

seq[1:4:2, 7:9]   # 元组中甚至可以有多个切片对象。
(slice(1, 4, 2), slice(7, 9, None))
```

关于slice：

```python
>>> slice
<class 'slice'>  # slice 是内置的类型

>>> dir(slice)
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'indices', 'start', 'step', 'stop']
```

slice 有 start、stop 和 step 数据属性，以及 indices 方法。

```python
help(slice.indices)
Help on method_descriptor:
indices(...)
    S.indices(len) -> (start, stop, stride)
    
    Assuming a sequence of length len, calculate the start and stop
    indices, and the stride(步幅) length of the extended slice described by
    S. Out of bounds indices are clipped(截断) in a manner consistent with the
    handling of normal slices.
```

indices 方法开放了内置序列实现的棘手逻辑，用于优雅地处理缺失索引和负数索引，以及长度超过目标序列的切片。这个方法会“整顿”元组，把 start、stop 和 stride 都变成非负数，而且都落在指定长度序列的边界内。

```python
slice(None, 10, 2).indices(5)
(0, 5, 2)
slice(-3, None, None).indices(5)
(2, 5, 1)

'ABCDE'[:10:2] 
'ACE'
'ABCDE'[-3:]
'CDE'
```

---

#### 5. 能处理切片的 `__getitem__` 方法

```python
import math
import numbers
import reprlib
from array import array

class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._classname = type(self).__name__  # Vector
        self._components = array(self.typecode, components)  # array('d', [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)  # "array('d', [1.0, 2.0, 3.0, 4.0, 5.0, ...])"
        components = components[components.find('['):-1]
        return f'{self._classname}({components})'

    def __str__(self):
        return f'{self._classname}({list(self)})'

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))
        # 这里不能像abs和bool函数里写的那样直接写self，会导致循环调用__bytes__

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])  # d b'd\x00\x00\x00\x0.....
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

    def __len__(self):
        return len(self._components)

		# 主要是__getitem__函数的修改
    def __getitem__(self, index):
        cls = type(self)  # <class '__main__.Vector'>
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = f'{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))


vector = Vector(range(7))
print(repr(vector))  # Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])
print(vector)  # Vector([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
print(len(vector))  # 7
print(vector[0])  # 0.0
print(vector[1:3])  # Vector([1.0, 2.0])
print(vector.frombytes(bytes(vector)))  # Vector([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
```

---

#### 6. 动态存取属性

在 Vector2d 中，使用 @property 装饰器把 x 和 y 标记为只读特性（以前的例子）。我们可以在Vector 中编写四个特性，但这样太麻烦。特殊方法 `__getattr__` 提供了更好的方式。属性查找失败后，解释器会调用 `__getattr__` 方法：

- 对于 `my_obj.x` 表达式，Python会检查 `my_obj` 实例有没有名为 `x` 的属性；
- 若没有，到类（`my_obj.__class__`）中查找 (可查阅 `dir(vector.__class__` )；
- 若仍没有，顺着继承树继续查找；
- **若依旧找不到，调用 my_obj 所属类中定义的 `__getattr__` 方法**，传入 self 和属性名称的字符串形式（如 'x'）。

```python
class Vector:
    typecode = 'd'
    shortcut_name = 'xyzw'

    def __init__(self, components):
        self.cls = type(self)  # <class '__main__.Vector'>
        self._classname = self.cls.__name__  # Vector
        self._components = array(self.typecode, components)  

    # 属性查找失败后，解释器会调用 __getattr__ 方法
    def __getattr__(self, item):
        if len(item) == 1 and item in self.shortcut_name:
            return self._components[self.shortcut_name.index(item)]
        # if len(item) == 1:
        #     index = self.cls.shortcut_name.find(item)
        #     if 0 <= index < len(self._components):
        #         return self._components[index]
        else:
            msg = f'{self.cls} object has no attribute {item}'
            raise AttributeError(msg)
            
     # 省略其他函数
    
vector = Vector(range(1,7))
print(vector.x)  # 1.0  使用 vector.x 获取第一个元素（v[0]）
vector.x = 10    # 为 vector.x 赋新值，这个操作应该抛出异常。
print(vector.x)  # 10   向量的分量没变。
print(vector)    # Vector([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
```

最后打印vector，发现向量的分量数组中没有新值，为什么 vector.x 返回10 ？之所以前后矛盾，是 `__getattr__` 的运作方式导致的：

仅当对象没有指定名称的属性时，Python 才会调用 `__getattr__` 方法，这是一种后备机制。可是，像 v.x  =  10 这样赋值之后，v 对象有 x 属性了，因此使用 v.x 获取 x 属性的值时不会调用 `__getattr__` 方法了，解释器直接返回绑定到 v.x 上的值，即 10。另一方面，`__getattr__` 方法的实现没有考虑到`self._components` 之外的实例属性，而是从这个属性中获取 `shortcut_names` 中所列的“虚拟属性”。

如何才能处理上述现象，使用 `__setattr__`，避免这种前后矛盾的现象，需要改写 Vector 类中设置属性的逻辑。 之前是使用 @property 装饰器把 x 和 y 标记为只读特性，现在不使用这种方式，但是想达到的目的是一样的：如果为 .x 或 .y 实 例 属 性 赋 值， 会 抛 出AttributeError；为了避免歧义，在 Vector 类中，如果为名称是单个小写字母的属性赋值，我们也想抛出那个异常。为此，我们要实现 `__setattr__` 方法：

```python
class Vector:
    typecode = 'd'
    shortcut_name = 'xyzw'

    def __init__(self, components):
        self.cls = type(self) 
        self._classname = self.cls.__name__  
        self._components = array(self.typecode, components)  

    def __getattr__(self, item):
        if len(item) == 1 and item in self.shortcut_name:
            return self._components[self.shortcut_name.index(item)]
        else:
            msg = f'{self._classname} object has no attribute: {item}'
            raise AttributeError(msg)

    def __setattr__(self, key, value):
        if len(key) == 1:  # 这里只特别处理名称是单个字符的属性
            if key in self.cls.shortcut_name:
                error = f'readonly attribute {self._classname}'
            elif key.islower():
                error = f'can\'t set attrbute "a" to "z" in {self._classname}'
            else:
                error = ''
            if error:
                raise AttributeError(error)
        super().__setattr__(key, value)  # 默认情况：在超类上调用 __setattr__ 方法，提供标准行为。
       
    # 省略其他函数
    
vector = Vector(range(1,7))

# print(vector.a)  # AttributeError: Vector object has no attribute: a
print(vector.x)  # 1.0
vector.x = 10  # AttributeError: readonly attribute Vector
# vector.a = 10  # AttributeError: can't set attrbute "a" to "z" in Vector
# vector.A = 10
# print(vector.A)  # 10
```

抄注：super() 函数用于动态访问超类的方法，对 Python 这样支持多重继承的动态语言来说，必须能这么做。程序员经常使用这个函数把子类方法的某些任务委托给超类中适当的方法。

---

#### 7. 散列和快速等值测试

计算聚合异或的 3 种方式：一种使用 for 循环，两种使用 reduce 函数：

```python
import functools
import operator

n = 0

for i in range(6):
    n ^= i
print(n)

print(functools.reduce(lambda a, b: a ^ b, range(6)))

print(functools.reduce(operator.xor, range(6)))
```

注：operator 模块以函数的形式提供了 Python 的全部中缀运算符，从而减少使用 lambda 表达式。

再次实现 ` __hash__  `方法，加上现有的 ` __eq__ `方法，这会把 Vector 实例变成可散列的对象。之前的示例中的 `__hash__` 方法简单地计算 `hash(self.x) ^ hash(self.y)`。这一次，我们要使用 ^（异或）运算符依次计算各个分量的散列值，像这样：v[0]  ^  v[1]  ^  v[2]...。这正是 `functools.reduce` 函数的作用。之前说 reduce 没有以往那么常用，但是计算向量所有分量的散列值非常适合使用这个函数。

```python
class Vector:
    typecode = 'd'
    shortcut_name = 'xyzw'

    def __init__(self, components):
        self.cls = type(self)  # <class '__main__.Vector'>
        self._classname = self.cls.__name__  # Vector
        self._components = array(self.typecode, components) 
        
    def __iter__(self):
        return iter(self._components)
    # 省略其他函数
    
    def __len__(self):
        return len(self._components)
      
    def __hash__(self):
        hashed = (hash(x) for x in self._components)  # 创建生成器表达式，惰性计算各个分量的散列值。
        return functools.reduce(operator.xor, hashed, 0)  # 把hashed给reduce 函数，使用xor函数计算聚合的散列值；第三个参数，0是初始值。
    
vector = Vector(range(1,7))
```

注：使用 reduce 函数时最好提供第三个参数，`reduce(function,  iterable, initializer)`，这样能避免这个异常：TypeError: reduce() of empty sequence with  no  initial  value。如果序列为空，initializer 是返回的结果；否则，在归约中使用它作为第一个参数，因此应该使用恒等值。比如，对 +、| 和 ^ 来说，initializer 应该是 0；而对 * 和 & 来说，应该是 1。

修改 ` __eq__` 方法，减少处理时间和内存用量——对大型向量来说：

```python
def __eq__(self, other):
    # return tuple(self) == tuple(other)  # 对于多维向量比较太耗时、低效

    if len(self) != len(other):
        return False
    for a, b in zip(self, other):  # zip 函数生成一个由元组构成的生成器
        if a != b:
            return False
    return True

```

用于计算聚合值的整个 for 循环可以替换成一行 all 函数调用：如果所有分量对的比较结果都是 True，那么结果就是 True。只要有一次比较的结果是False，all 函数就返回 False。

```python
def __eq__(self, other):
		# 使用聚合函数 all
		return len(self) == len(other) and all(a == b for a, b in zip(self, other))
```
首先要检查两个操作数的长度是否相同，因为 zip 函数会在最短的那个操作数耗尽时停止。

关于 zip 函数：

内置的 zip 函数。使用 zip 函数能轻松地并行迭代两个或更多可迭代对象，它返回的元组可以拆包成变量，分别对应各个并行输入中的一个元素。zip 函数的名字取自拉链系结物（zipper fastener），因为这个物品用于把两个拉链边的链牙咬合在一起，这形象地说明了 zip(left,  right) 的作用。zip 函数与文件压缩没有关系。

```python
>>> zip(range(3), 'abc')
<zip object at 0x0000023375683D08>

>>> list(zip(range(3), 'abc'))
[(0, 'a'), (1, 'b'), (2, 'c')]

>>> list(zip(range(3), 'abc', [0.0, 1.1, 2.2, 3.3]))
[(0, 'a', 0.0), (1, 'b', 1.1), (2, 'c', 2.2)]

>>> from itertools import zip_longest
>>> list(zip_longest(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3], fillvalue=-1))
[(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2), (-1, -1, 3.3)]
```

