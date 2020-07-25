

## 继承的优缺点

#### 1. 子类化内置类型很麻烦

在Python3中，内置类型可以子类化，但是有个重要的注意事项：**内置类型（CPython）不会调用用户定义的类覆盖的特殊方法。**

内置类型的方法不会调用子类覆盖的方法。例如，dict 的子类覆盖的 `__getitem__()` 方法不会被内置类型的 `get()` 方法调用。

```python
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [key] * 2)


d = DoppelDict(one=1)
d["two"] = 2
d.update(three=3)
print(d)
# {'one': 1, 'two': ['two', 'two'], 'three': 3}
```

可以看出继承自 dict 的 `__init__` 、`update` 方法显然忽略了覆盖的 `__setitem__` 方法，[] 运算符会调用覆盖的 `__setitem__`  方法。

原生类型的这种行为违背了**面向对象编程的一个基本原则：始终应该从实例（self）所属的类开始搜索方法，即使在超类实现的类中调用也是如此**。在这种糟糕的局面中， `__missing__` 方法却能按预期方式工作，不过这只是特例。

不只实例内部的调用有这个问题（`self.get()` 不调用 `self.__getitem__()`），**内置类型的方法调用的其他类的方法，如果被覆盖了，也不会被调用。**

```python
class answerDict(dict):
    def __getitem__(self, item):
        return 100

ad = answerDict(one=1)
print(ad["one"])  # 100  不管传入什么键，AnswerDict.__getitem__ 方法始终返回100。
new_ad = {}
new_ad.update(ad)
print(new_ad)  # {'one': 1}
print(new_ad["one"])  # 1  dict.update 方法忽略了AnswerDict.__getitem__方法。
```

小结：**直接子类化内置类型（如 dict、list 或 str）容易出错，因为内置类型的方法通常会忽略用户覆盖的方法。不要子类化内置类型，用户自己定义的类应该继承 collections 模块中的类，例如 UserDict、UserList 和 UserString，这些类做了特殊设计，因此易于扩展。**

```python
from collections import UserDict

class DoppelDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [key] * 2)

class answerDict(UserDict):
    def __getitem__(self, item):
        return 100
```

---

#### 2. 多重继承和方法解析顺序

任何实现多重继承的语言都要处理潜在的命名冲突，这种冲突由不相关的祖先类实现同名方法引起。

![image-20200208192102700](../../../markdown_pic/java_inheritance_multiple.png)

```python
class A:
    def ping(self):
        print("A ping", self)

class B(A):
    def pong(self):
        print("B pong", self)

class C(A):
    def pong(self):
        print("C pong", self)

class D(B, C):
    def ping(self):
        super().ping()
        print("D ping", self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)

d = D()

# 直接调用 d.pong() 运行的是 B 类中的版本
d.pong()  # B pong <__main__.D object at 0x000001984DC16AC8>

# 超类中的方法都可以直接调用，此时要把实例作为显式参数传入
C.pong(d) # C pong <__main__.D object at 0x000001984DC16AC8>
B.pong(d) # B pong <__main__.D object at 0x000001984DC16AC8>
```

Python 能区分 d.pong() 调用的是哪个方法，是因为 Python 会按照特定的顺序遍历继承图。这个顺序叫**方法解析顺序**（Method Resolution Order，**MRO**）。类都有一个名为 `__mro__` 的属性，它的值是一个元组，按照方法解析顺序列出各个超类，从当前类一直向上，直到object 类。有了这一机制，继承方法的名称不再会发生冲突。

```python
print(D.__mro__)
# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)

print(bool.__mro__)  # 可以看出 bool 从 int 和 object 中继承方法和属性。
# (<class 'bool'>, <class 'int'>, <class 'object'>)
```

若想把方法调用委托给超类，推荐的方式是使用内置的 super() 函数。然而，有时可能需要绕过方法解析顺序，直接调用某个超类的方法——这样做有时更方便。例如，D.ping 方法可以这样写：

```python
    def ping(self):
        # super().ping()
        A.ping(self)  # 直接在类上调用实例方法时，必须显式传入self参数，因为这样访问的是未绑定方法（unbound method）
        print("D ping", self)
```

使用 super() 最安全，也不易过时。调用框架或不受自己控制的类层次结构中的方法时，尤其适合使用 super()。使用 super() 调用方法时，会遵守方法解析顺序。

```python
d.ping()
# A ping <__main__.D object at 0x0000026DB0765B38>
# D ping <__main__.D object at 0x0000026DB0765B38>
```

```python
    def pingpong(self):
        self.ping()  # A ping、D ping、
        super().ping()  # A ping
        self.pong()  # B pong
        super().pong()  # B pong
        C.pong(self)  # C pong
```

其中，第三个调用是 self.pong()，根据 `__mro__`，找到的是 B 类实现的 pong 方法。第四个调用是 super().pong()，也根据 `__mro__`，找到 B 类实现的 pong 方法。第五个调用是 C.pong(self)，忽略 `__mro__`，找到的是 C 类实现的 pong 方法。

**方法解析顺序不仅考虑继承图，还考虑子类声明中列出超类的顺序**。也就是说，如果在把 D 类声明为 `class  D(C,  B):`，那么 D 类的 `__mro__` 属性就会不一样：先搜索 C 类，再搜索 B 类。

