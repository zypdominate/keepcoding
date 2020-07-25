## 属性描述符

描述符是对多个属性运用相同存取逻辑的一种方式。例如，Django ORM和SQL Alchemy等ORM中的字段类型是描述符，把数据库记录中字段里的数据与Python对象的属性对应起来。

描述符是实现了特定协议的类，这个协议包括 `__get__`、`__set__`和 `__delete__` 方法。property类实现了完整的描述符协议。通常，可以只实现部分协议。其实，我们在真实的代码中见到的大多数描述符只实现了 `__get__` 和 `__set__` 方法，还有很多只实现了其中的一个。

描述符是Python的独有特征，不仅在应用层中使用，在语言的基础设施中也有用到。除了特性之外，使用描述符的Python功能还有方法及classmethod和staticmethod装饰器。理解描述符是精通Python的关键。

---

#### 1. 描述符示例：验证属性

实现了 `__get__`、`__set__` 或 `__delete__` 方法的类是描述符。**描述符的用法是，创建一个实例，作为另一个类的类属性。**

将定义一个Quantity描述符，LineItem类会用到两个Quantity实例：一个用于管理weight属性，另一个用于管理price属性。示意图有助于理解，如图所示:

![image-20200404212558097](../../../markdown_pic/book2_Quantity.png)

在图中，“weight”这个词出现了两次，因为其实有两个不同的属性都叫weight：一个是LineItem的类属性，另一个是各个LineItem对象的实例属性。price也是如此。

**描述符类**：实现描述符协议的类。图中的Quantity类。

**托管类**：把描述符实例声明为类属性的类。图中的LineItem类。

**描述符实例**：描述符类的各个实例，声明为托管类的类属性。在图中，各个描述符实例使用箭头和带下划线的名称表示（在UML中，下划线表示类属性）。与黑色菱形接触的LineItem类包含描述符实例。

**托管实例**：托管类的实例。在这个示例中，LineItem实例是托管实例。

**储存属性**：托管实例中存储自身托管属性的属性。在图中，LineItem实例的weight和price属性是储存属性。这种属性与描述符实例不同，描述符属性都是类属性。

**托管属性**：托管类中由描述符实例处理的公开属性，值存储在储存属性中。也就是说，描述符实例和储存属性为托管属性建立了基础。

Quantity实例是LineItem类的类属性，这一点一定要理解。

```python
class Quantity:  # 描述符基于协议实现，无需创建子类
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must >0')


class LineItem:
    weight = Quantity('weight')  # 第一个描述符实例绑定给weight属性
    price = Quantity('price')	 # 第二个描述符实例绑定给price属性

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
```

在 Quantity 类中：

`self.storage_name = storage_name` ：表示Quantity实例有个storage_name属性，这是托管实例中存储值的属性的名称。

`__set__` 函数：尝试为托管属性赋值时，会调用 `__set__` 方法。这里，self 是描述符实例（即LineItem.weight 或 LineItem.price），instance是托管实例（LineItem实例），value是要设定的值。

另外，必须直接处理托管实例的 `__dict__` 属性；如果使用内置的setattr函数，会再次触发 `__set__` 方法，导致无限递归。

各个托管属性的名称与储存属性一样，而且读值方法不需要特殊的逻辑，所以Quantity类不需要定义`__get__` 方法。

编写 `__set__` 方法时，要记住 self 和 instance 参数的意思：self 是描述符实例，instance 是托管实例。管理实例属性的描述符应该把值存储在托管实例中。因此，Python才为描述符中的那个方法提供了instance 参数。

**self 是描述符实例，它其实是托管类的类属性。同一时刻，内存中可能有几千个LineItem实例，不过只会有两个描述符实例：LineItem.weight 和 LineItem.price。因此，存储在描述符实例中的数据，其实会变成LineItem类的类属性，从而由全部LineItem实例共享。**

---

#### 2. 自动获取储存属性的名称

为了避免在描述符声明语句中重复输入属性名，我们将为每个Quantity实例的storage_name属性生成一个独一无二的字符串。更新后的Quantity和LineItem类的UML类图：

![image-20200405000039530](../../../markdown_pic/book2_Quantity2.png)

为了生成storage_name，我们以`'_Quantity#'`为前缀，然后在后面拼接一个整数：`Quantity.__counter`类属性的当前值，每次把一个新的Quantity描述符实例依附到类上，都会递增这个值。在前缀中使用井号能避免storage_name与用户使用点号创建的属性冲突，因为nutmeg._Quantity#0是无效的Python句法。但是，内置的getattr和setattr函数可以使用这种“无效的”标识符获取和设置属性，此外也可以直接处理实例属性__dict__。

```python
class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__  # cls是Quantity类的引用。
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f'_{prefix}#{index}'  # 每个描述符实例的storage_name属性都是独一无二的
        print(self.storage_name)
        cls.__counter += 1

    def __get__(self, instance, owner):
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must > 0')


class LineItem:
    weight = Quantity()  # 不用把托管属性的名称传给Quantity构造方法。
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    item = LineItem('test', 10, 20)
    print(f'weight:{item.weight}, price:{item.price}')
    print(getattr(item, '_Quantity#0'), getattr(item, '_Quantity#1'))
    '''
    _Quantity#0
    _Quantity#1
    weight:10, price:20
    10 20
    '''
```

这里可以使用内置的高阶函数getattr和setattr存取值，无需使用 `instance.__dict__`，因为托管属性和储存属性的名称不同，所以把储存属性传给getattr函数不会触发描述符，不会像上一个那样出现无限递归。

---

注意，`__get__` 方法有三个参数：self、instance和owner。owner参数是托管类（如LineItem）的引用，通过描述符从托管类中获取属性时用得到。*如果使用 LineItem.weight 从类中获取托管属性（以weight为例），描述符的 `__get__` 方法接收到的instance参数值是None*。因此，下述控制台会话才会抛出AttributeError异常：

```python
item = LineItem('test', 10, 20)
print(LineItem.weight)
```

```shell
......
	print(LineItem.weight)
  File "D:/keeplearning/myLearning/python/book2/a6_2_QuantityLineItem2.py", line 13, in __get__
    return getattr(instance, self.storage_name)
AttributeError: 'NoneType' object has no attribute '_Quantity#0'
```

抛出AttributeError异常是实现 `__get__` 方法的方式之一，如果选择这么做，应该修改错误消息，去掉令人困惑的NoneType和_Quantity#0，这是实现细节。把错误消息改成"'LineItem' class has no such attribute"更好。最好能给出缺少的属性名，但是在这个示例中，描述符不知道托管属性的名称，因此目前只能做到这样。此外，为了给用户提供内省和其他元编程技术支持，通过类访问托管属性时，最好让 `__get__` 方法返回描述符实例。如下做了小幅改动，为 `Quantity.__get__` 方法添加了一些逻辑：

```python
def __get__(self, instance, owner):
    if instance is None:  # 如果不是通过实例调用，返回描述符自身。
        return self
    return getattr(instance, self.storage_name)
```

此时：

```python
item = LineItem('test', 10, 20)
print(LineItem.weight)
# <__main__.Quantity object at 0x00000187E175FA58>
```

可能觉得就为了管理几个属性而编写这么多代码不值得，但是要知道，描述符逻辑现在被抽象到单独的代码单元（Quantity类）中了。通常，我们不会在使用描述符的模块中定义描述符，而是在一个单独的实用工具模块中定义，以便在整个应用中使用——如果开发的是框架，甚至会在多个应用中使用。

---

描述符的常规用法：

```python
# model.py
class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f'_{prefix}#{index}'
        print(self.storage_name)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:  # 如果不是通过实例调用，返回描述符自身。
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must > 0')
```

```python
import model  # 描述符常规用法：将描述符从另一个模块中导入

class LineItem:
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
```

就目前的实现来说，Quantity描述符能出色地完成任务。它唯一的缺点是，储存属性的名称是生成的（如_Quantity#0），导致用户难以调试。但这是不得已而为之，如果想自动把储存属性的名称设成与托管属性的名称类似，需要用到类装饰器或元类。

描述符在类中定义，因此可以利用继承重用部分代码来创建新描述符。

---

#### 3. 一种新型描述符

虚构的有机食物网店遇到一个问题：不知怎么回事儿，有个商品的描述信息为空，导致无法下订单。为了避免出现这个问题，我们要再创建一个描述符，NonBlank。在设计NonBlank的过程中，我们发现，它与Quantity描述符很像，只是验证逻辑不同。

回想 Quantity 的功能，我们注意到它做了两件不同的事：**管理托管实例中的储存属性，以及验证用于设置那两个属性的值**。由此可知，可以重构，并创建两个基类。

AutoStorage：自动管理储存属性的描述符类。

Validated：扩展AutoStorage类的抽象子类，覆盖 `__set__` 方法，调用必须由子类实现的validate方法。

![image-20200405132615175](../../../markdown_pic/book2_Quantity3_refactor.png)

Validated、Quantity和NonBlank三个类之间的关系体现了模板方法设计模式。具体而言，`Validated.__set__`方法是这种模板方法的例证：**一个模板方法用一些抽象的操作定义一个算法，而子类将重定义这些操作以提供具体的行为。**

这里，抽象的操作是验证：

```python
# model.py
import abc

class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f'_{prefix}#{index}'
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        '''return validated value or raise ValueError'''
        pass


class Quantity(Validated):
    """a number bigger than zero"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must > 0')
        return value


class NoneBlank(Validated):
    '''a string with at least one none-space character'''

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value
```

```python
import model

class LineItem:
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    item = LineItem('test', 10, 20)
    print(LineItem.weight)
    print(f'weight:{item.weight}, price:{item.price}')
    print(getattr(item, '_Quantity#0'), getattr(item, '_Quantity#1'))
    '''
    <__main__.Quantity object at 0x000002D5D1C8B9B0>
    weight:10, price:20
    10 20
    '''
```

LineItem示例演示了描述符的典型用途——**管理数据属性**。这种描述符也叫**覆盖型描述符**，因为描述符的`__set__`方法使用托管实例中的同名属性覆盖（即插手接管）了要设置的属性。不过，也有非覆盖型描述符。