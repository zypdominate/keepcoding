## 符合Python风格的对象

#### 1. 对象表示形式

每门面向对象的语言至少都有一种获取对象的字符串表示形式的标准方式。Python 提供了两种方式。

- **repr()** : 以便于**开发者**理解的方式返回对象的字符串表示形式。

- **str()** : 以便于**用户**理解的方式返回对象的字符串表示形式。

在 Python 3 中，`__repr_`_、`__str__ `和`__format__ `都必须返回 Unicode 字符串（str 类型），只有 `__bytes__` 方法应该返回字节序列（bytes 类型）。

---

#### 2. 向量类的示例：

```python
import math
from array import array

class Vector2d(object):
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):   # TypeError: 'Vector2d' object is not iterable
        return (i for i in (self.x, self.y))  # a, b = v

    def __str__(self):
        return "str:" + str(tuple(self))  # print(v)

    def __repr__(self):
        class_name = type(self).__name__
        return f'{class_name}({self.x},{self.y})'  # repr(v)
        # return '{}({!r},{!r})'.format(class_name, *self)  # repr(v)
        # return f'repr:{class_name}({self.x},{self.y})'  # repr(v)

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode,self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __call__(self, *args, **kwargs):
        return self
```

```python
v = Vector2d(3, 4)
print(v.x ,v.y)  # Vector2d 实例的分量可以直接通过属性访问（无需调用读值方法）。
# 3.0 4.0

x, y = v  # 拆包成变量元组
x, y
# (3.0, 4.0)

v  # repr 函数调用 Vector2d 实例，得到的结果类似于构建实例的源码。
# Vector2d(3.0,4.0)

v_clone = eval(repr(v)) # 使用eval函数，表明repr函数调用Vector2d实例得到的是对构造方法的准确表述。
v == v_clone   # Vector2d 实例支持使用 == 比较；这样便于测试
# True
v_clone.x ,v_clone
# (3.0, 4.0)

print(v)  # print 函数会调用 str 函数，对 Vector2d 来说，输出的是一个有序对。
# str:(3.0, 4.0)

bytes(v)
# b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
abs(v)
# 5.0

bool(v), bool(Vector2d(0, 0))
# (True, False)
```

---

#### 3. classmethod与staticmethod

classmethod 用法：定义操作类，而不是操作实例的方法。classmethod 改变了调用方法的方式，因此类方法的第一个参数是类本身，而不是实例。classmethod 最常见的用途是定义备选构造方法。按照约定，类方法的第一个参数名为 cls。

staticmethod 装饰器也会改变方法的调用方式，但是第一个参数不是特殊的值。其实，静态方法就是普通的函数，只是碰巧在类的定义体中，而不是在模块层定义。

```python
class Demo():
    @classmethod
    def cls_method(*args):
        return args

    @staticmethod
    def static_method(*args):
        return args

print(Demo.cls_method())  # (<class '__main__.Demo'>,)
print(Demo.cls_method('a'))  # (<class '__main__.Demo'>, 'a')

print(Demo.static_method())  # () 
print(Demo.static_method('b'))  # ('b',)  
```

classmethod 装饰器非常有用，但是从未见过不得不用 staticmethod 的情况。如果想定义不需要与类交互的函数，那么在模块中定义就好了。有时，函数虽然从不处理类，但是函数的功能与类紧密相关，因此想把它放在近处。即便如此，在同一模块中的类前面或后面定义函数也就行了。

---

#### 4. 格式化显示

内置的 format() 函数和 str.format() 方法把各个类型的格式化方式委托给相应的

`.__format__(format_spec) `方法。format_spec 是**格式说明符**，它是：

- format(my_obj, format_spec) 的第二个参数，或者

- str.format() 方法的格式字符串，{} 里代换字段中冒号后面的部分

```python
brl = 1 / 2.43  # BRL到USD的货币兑换比价
brl
# 0.4115226337448559
format(brl, '0.4f')
# '0.4115'
'1 BRL = {rate:0.2f} USD'.format(rate=brl)
# '1 BRL = 0.41 USD'
```

格式说明符是'0.4f'、 '0.2f'。代换字段中的 'rate' 子串是字段名称，与格式说明符无关，但是它决定把 .format() 的哪个参数传给代换字段。

格式规范微语言为一些内置类型提供了专用的表示代码。比如，b 和 x 分别表示二进制和十六进制的 int 类型，f 表示小数形式的 float 类型， % 表示百分数形式：

```python
format(17, 'x')
# '11'
format(8, 'b')
# '1000'
format(2 / 5, '.1%')
# '40.0%'
format(2 / 5, '.1f')
# '0.4'
```

格式规范微语言是可扩展的，因为各个类可以自行决定如何解释 format_spec 参数。例如datetime 模块中的类，它们的 `__format__` 方法使用的格式代码与 strftime() 函数一样。下面是内置的 format() 函数和 str.format() 方法的几个示例：

```python
from datetime import datetime
now = datetime.now()
now
# datetime.datetime(2020, 1, 1, 20, 36, 45, 959123)
format(now, '%H:%M:%S')
# '20:36:45'
'now is {:%I:%M %p}'.format(now)
# 'now is 08:36 PM'
```

如果类没有定义` __format__ `方法，从 object 继承的方法会返回 str(my_object)。我们为Vector2d 类定义了 `__str__ `方法，因此可以这样做：

```python
class Vector2d(object):
  # 省略其他函数
	def __str__(self):
        return "str:" + str(tuple(self))  # print(v)

v = Vector2d(3, 4)
print(format(V))  # str:(3.0, 4.0)
print(format(v, '.3f'))  # 如果传入格式说明符，报错TypeError: unsupported format string passed to Vector2d.__format__
```

如果想要实现自己的微语言来处理这个报错，且想要的效果如下：

```python
print(format(v, '.3f'))
# (3.000, 4.000)
print(format(v, '.3e'))
# (3.000e+00, 4.000e+00)
```

```python
class Vector2d(object):
    # 省略其他函数
    def __format__(self, format_spec=''):
        # 使用内置的format函数把fmt_spec应用到向量的各个分量上，构建一个可迭代的格式化字符串
        components = (format(item, format_spec) for item in self)
        # 把格式化字符串代入公式 '(x, y)' 
        return '({}, {})'.format(*components)
```

---

#### 5. 可散列的Vector2d

为了把 Vector2d 实例变成可散列的，必须使用` __hash__ `方法（还需要 `__eq__ `方法，前面已经实现了）。此外，还要让向量不可变。

目前，我们可以为分量赋新值，如 v.x = 7，Vector2d 类的代码并不阻止这么做。为此，我们要把 x 和 y 分量设为只读特性，这样才能实现` __hash__ `方法。

```python
import math
from array import array

class Vector2d(object):
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)  # 属性标记为私有的
        self.__y = float(y)

    @property  # @property 装饰器把读值方法标记为特性
    def x(self):  # 读值方法与公开属性同名，都是x
        return self.__x

    @property
    def y(self):
        return self.__y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)  # 异或
      
    # 需要读取x和y分量的方法可保持不变，通过self.x和self.y读取公开特性，不必读取私有属性
    def __iter__(self):
        return (i for i in (self.x, self.y))
      
    def __eq__(self, other):
        return tuple(self) == tuple(other)
		# 其他函数省略
    
v = Vector2d(3, 4)
print(v.x, v.y)
v.x = 10  # AttributeError: can't set attribute
print(v.x)
```

hash方法应该返回一个整数，理想情况下还要考虑对象属性的散列值（`__eq__ `方法也要使用），因为相等的对象应该具有相同的散列值，**最好使用位运算符 异或（^）混合各分量的散列值**。添加 `__hash__ `方法之后，向量变成可散列的了：

```python
v1 = Vector2d(3, 4)
v2 = Vector2d(3.1, 4.1)
print(hash(v1))  # 7
print(hash(v2))  # 1031
```

要想**创建可散列的类型，不一定要实现特性，也不一定要保护实例属性，只需正确地实现 `__hash__` 和` __eq__ `方法即可**。但是，实例的散列值绝不应该变化，因此我们借机提到了只读特性。

---

#### 6. Python的私有属性和“受保护的”属性

 Python 有个简单的机制，能避免子类意外覆盖“私有”属性。

举个例子。有人编写了一个名为 Dog 的类，这个类的内部用到了 mood 实例属性，但是没有将其开放。现在，你创建了 Dog 类的子类：Beagle。如果你在毫不知情的情况下又创建了名为 mood 的实例属性，那么在继承的方法中就会把 Dog 类的 mood 属性覆盖掉。这是个难以调试的问题。

为了避免这种情况，如果以 ` __mood ` 的形式（两个前导下划线，尾部没有或最多有一个下划
线）命名实例属性，Python 会把属性名存入实例的 ` __dict__ ` 属性中，而且会在前面加上一
个下划线和类名。因此，对 Dog 类来说，`__mood `会变成 ` _Dog__mood` ；对 Beagle 类来说，会
变成 `_Beagle__mood` 。这个语言特性叫**名称改写**（name mangling）。

```python
class Vector2d(object):

    def __init__(self, x, y):
        self.__x = float(x)  # 属性标记为私有的
        self.__y = float(y)

v = Vector2d(3, 4)
print(v.__dict__)
# {'_Vector2d__x': 3.0, '_Vector2d__y': 4.0}

print(v._Vector2d__x)
# 3.0
```

名称改写是一种安全措施，不能保证万无一失：它的目的是避免意外访问，不能防止故意做错事。比如：只要知道改写私有属性名的机制，任何人都能直接读取私有属性——这对调试和序列化倒是有用。此外，只要编写 `v1._Vector__x  =  7` 这样的代码，就能轻松地为 Vector2d 实例的私有分量直接赋值。

Python 解释器不会对使用单个下划线的属性名做特殊处理，这不过是很多 Python 程序员严格遵守的约定，他们不会在类外部访问这种属性。 遵守使用一个下划线标记对象的私有属性很容易，就像遵守使用全大写字母编写常量那样容易。

---

#### 7. 使用`__slot__ `类属性节省空间

默认情况下，Python 在各个实例中名为 `__dict__` 的字典里存储实例属性。

**为了使用底层的散列表提升访问速度，字典会消耗大量内存。如果要处理数百万个属性不多的实例，通过` __slots__ `类属性，能节省大量内存，方法是让解释器在元组中存储实例属性，而不用字典。**

继承自超类的 ` __slots__ ` 属性没有效果。Python 只会使用各个类中定义的 `__slots__` 属性。

**定义` __slots__ ` 的方式是，创建一个类属性，使用 `__slots__` 这个名字，并把它的值设为一个字符串构成的可迭代对象，其中各个元素表示各个实例属性。**

```python
class Vector2d(object):

    # 这里使用元组，因为这样定义的__slots__中所含的信息不会变化
    __slots__ = ('__x', '__y')

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

v = Vector2d(3, 4)
print(v.__slots__)
# ('__x', '__y')

# print(v.__dict__)  # 有了__slot__后就没有__dict__属性了
# AttributeError: 'Vector2d' object has no attribute '__dict__'

print(v._Vector2d__x)
# 3.0
```

在类中定义 `__slots__ `属性的目的是告诉解释器：“这个类中的所有实例属性都在这里了。”这样，Python 会在各个实例中使用类似元组的结构存储实例变量，从而避免使用消耗内存的` __dict__ `属性。如果有数百万个实例同时活动，这样做能节省大量内存。

在类中定义` __slots__ `属性之后，实例不能再有` __slots__ `中所列名称之外的其他属性。这只是一个副作用，不是` __slots__ `存在的真正原因。不要使用 `__slots__ `属性禁止类的用户新增实例属性。`__slots__` 是用于优化的，不是为了约束程序员。

`__slots__` 属性有些需要注意的地方，而且不能滥用，不能使用它限制用户能赋值的属性。

总之，如果使用得当，`__slots__ `能显著节省内存，不过有几点要注意。

- 每个子类都要定义` __slots__ `属性，因为解释器会忽略继承的` __slots__ `属性。
- 实例只能拥有` __slots__ `中列出的属性，除非把` '__dict__' `加入 `__slots__` 中（这样做就失去了节省内存的功效）。
-  如果不把 `'__weakref__' `加入` __slots__`，实例就不能作为弱引用的目标。

---

#### 8. 覆盖类属性

Python 有个很独特的特性：**类属性可用于为实例属性提供默认值**。

```python
class Vector2d(object):
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))
```

Vector2d 中有个 typecode类属性，`__bytes__` 方法两次用到了它，而且都故意使用 self.typecode 读取它的值。因为Vector2d 实例本身没有 typecode 属性，所以 self.typecode 默认获取的是 Vector2d.typecode类属性的值。

但是，**如果为不存在的实例属性赋值，会新建实例属性**。假如我们为 typecode 实例属性赋值，那么**同名类属性不受影响**。然而，自此之后，实例读取的 self.typecode 是实例属性typecode，也就是**把同名类属性遮盖了**。借助这一特性，可以为各个实例的 typecode 属性定制不同的值。

```python
class Vector2d(object):
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

v = Vector2d(3, 4)
print(v.typecode)  # d

v.typecode = 'f'
print(v.typecode)   # f
print(Vector2d.typecode)  # d
```

如果想修改类属性的值，必须直接在类上修改，不能通过实例修改。如果想修改所有实例（没有 typecode 实例变量）的 typecode 属性的默认值，可以这么做：`Vector2d.typecode = 'e' `。

有种修改方法更符合 Python 风格，而且效果持久，也更有针对性。类属性是公开的，因此会被子类继承，于是经常会创建一个子类，只用于定制类的数据属性。Django 基于类的视图就大量使用了这个技术。

```python
class Vector2d(object):
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        # 没有硬编码class_name的值，而是使用type(self).__name__获取
        self.class_name = type(self).__name__

    def __str__(self):
        return f"str：{self.class_name}" + str(tuple(self))  # print(v)
      
      
#  把 ShortVector2d 定义为 Vector2d 的子类，只用于覆盖 typecode 类属性
class ShortVector2d(Vector2d):
    typecode = 'f'

sv = ShortVector2d(1,2)
print(sv)  # str：ShortVector2d(1.0, 2.0)
print(sv.typecode)  # s
```

同时，如果硬编码 class_name 的值，那么 Vector2d 的子类（如 ShortVector2d）要覆盖` _str__`方法。从实例的类型中读取类名，`__str__ `方法就可以放心继承。

最后小结一下就是，通过一个简单的类Vector说明了如何利用数据模型处理 Python 的其他功能：提供不同的对象表示形式、实现自定义的格式代码、公开只读属性，以及通过 hash() 函数支持集合和映射。