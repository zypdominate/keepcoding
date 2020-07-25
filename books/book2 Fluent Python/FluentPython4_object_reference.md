## 对象引用、可变性和垃圾回收

#### 1. 变量不是盒子

人们经常使用“变量是盒子”这样的比喻解释变量，但是这有碍于理解面向对象语言中的引用式变量。Python 变量类似于 Java 中的引用式变量，因此最好把它们理解为附加在对象上的标注。

```python
class Gi():
    def __init__(self):
        print(f'Gi id:{id(self)}')
        
gi = Gi()
# Gi id:2323558943432
gi2 = Gi()
# Gi id:2323559105872
```

变量只不过是标注，所以无法阻止为对象贴上多个标注。贴的多个标注，就是别名。

---

#### 2. 标识、相等性和别名

```python
tom = {'name':'TOM', 'age':10, 'sex':'m'}
tomy = tom

tomy is tom
# True
id(tomy), id(tom)
# (2323559005352, 2323559005352)
tomy == tom
# True
  
tam = {'name':'TOM', 'age':10, 'sex':'m'}

tom is tam
# False
id(tom), id(tam)
# (2323559005352, 2323558896264)
tom == tam
# True
```

tomy和tom 是别名，即两个变量绑定同一个对象`{'name':'TOM', 'age':10, 'sex':'m'}`。而 tam 不是 tom的别名，因为二者绑定的是不同的对象。tam 和 tom 绑定的对象具有相同的值（== 比较的就是值），但是它们的标识不同。

**每个变量都有标识、类型和值。**

- **对象一旦创建，它的标识绝不会变；**
- **可以把标识理解为对象在内存中的地址。**
- **is 运算符比较两个对象的标识；**
- **id() 函数返回对象标识的整数表示。**

编程中很少使用 id() 函数。标识最常使用 is 运算符检查，而不是直接比较 ID。

---

#### 3. 在**==**和is之间选择

== 运算符比较两个对象的值（对象中保存的数据），而 is 比较对象的标识。

通常，我们关注的是值，而不是标识，因此 Python 代码中 == 出现的频率比 is 高。

在变量和单例值之间比较时，应该使用 is。目前，最常使用 is 检查变量绑定的值是不是 None。推荐的写法：`x is None`，否定的正确写法是：`x is not None `。

**is 运算符比 == 速度快，因为它不能重载**，所以 Python 不用寻找并调用特殊方法，而是直接比较两个整数 ID。而 a == b 是语法糖，等同于` a.__eq__(b)`。继承自 object 的` __eq__`方法比较两个对象的 ID，结果与 is 一样。但是多数内置类型使用更有意义的方式覆盖了`__eq__` 方法，会考虑对象属性的值。相等性测试可能涉及大量处理工作，例如，比较大型集合或嵌套层级深的结构时。

---

#### 4. 元组的相对不可变性

元组与多数 Python 集合（列表、字典、集，等等）一样，**保存的是对象的引用**。如果**引用的元素是可变的，即便元组本身不可变，元素依然可变**。也就是说，**元组的不可变性其实是指 tuple 数据结构的物理内容**（即保存的引用）不可变，与引用的对象无关。

```python
t1 = (1,2,[3,4,5])
t2 = (1,2,[3,4,5])
t1 == t2
# True
id(t1[-1])  
# 2323559065032
t1[-1].append(0)   # t1 不可变，但是 t1[-1] 可变
id(t1[-1])
# 2323559065032   t1[-1] 的标识没变
t1 == t2  
# False   t1[-1]只是值变了, 导致t1不等于t2。
```

可以说，元组具有相对不可变性，这也是有些元组（元素中有可变的类型）不可散列的原因。

---

#### 5. 默认做浅复制

复制列表（或多数内置的可变集合）最简单的方式是使用内置的类型构造方法。

```python
l1 = [1, [2, 3, 4], (5, 6, 7)]
l2 = list(l1)

l1 is l2
# False
l1 == l2
# True
id(l1), id(l2)
# (2323559065672, 2323561081096)
```

对列表和其他可变序列来说，还能使用简洁的 l2 = l1[:] 语句创建副本。然而，构造方法或 [:] 做的是浅复制（即复制了最外层容器，副本中的元素是源容器中元素的引用）。如果所有元素都是不可变的，那么这样没有问题，还能节省内存。但是，如果有可变的元素，可能就会导致意想不到的问题。

```python
l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)
l1.append(100)
l1[1].remove(55)  # l2[1] 绑定的列表与 l1[1] 是同一个
print('l1:', l1) 
print('l2:', l2)
# l1: [3, [66, 44], (7, 8, 9), 100]
# l2: [3, [66, 44], (7, 8, 9)]
l2[1] += [33, 22]   # += 运算符就地修改列表
l2[2] += (10, 11)   # += 运算符创建一个新元组，然后重新绑定给变量 l2[2]
print('l1:', l1) 
print('l2:', l2)
# l1: [3, [66, 44, 33, 22], (7, 8, 9), 100]
# l2: [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]
```

---

#### 6.为任意对象做深复制和浅复制 

演示 copy() 和 deepcopy() 的用法：

```python
import copy
class Bus(object):
    def __init__(self, passengers = None):
        if passengers is None:
            self.passagers = []
        else:
            self.passagers = list(passengers)
    def up(self, someone):
        if someone in self.passagers:
            assert 0, f'{someone} is in bus already'
        self.passagers.append(someone)
    def down(self, someone):
        if someone not in self.passagers:
            assert 0, f'{someone} is not in bus now'
        self.passagers.remove(someone)
        
bus1 = Bus(['a','b','c','d'])
bus2 = copy.copy(bus1)   # 浅复制副本（bus2）
bus3 = copy.deepcopy(bus1)  # 是深复制副本（bus3）
```

```python
id(bus1), id(bus2), id(bus3)
# (2057602206352, 2057602063440, 2057602206296)

id(bus1.passagers), id(bus2.passagers), id(bus3.passagers)
# (2057599601928, 2057599601928, 2057599601736)

bus1.down('d')
print(bus1.passagers, bus2.passagers, bus3.passagers)
# ['a', 'b', 'c'] ['a', 'b', 'c'] ['a', 'b', 'c', 'd']
```

观察 passengers 属性后发现，bus1 和 bus2 共享同一个列表对象，因为 bus2 是 bus1 的浅复制副本。bus3 是 bus1 的深复制副本，因此它的 passengers 属性指代另一个列表。

一般来说，深复制不是件简单的事。如果对象有循环引用，那么这个朴素的算法会进入无限循环。deepcopy 函数会记住已经复制的对象，因此能优雅地处理循环引用。

```python
a = [1,2]
b = [a, 0]
a.append(b)
a
# [1, 2, [[...], 0]]
```

---

#### 7. 函数的参数作为引用时

Python 唯一支持的参数传递模式是 **共享传参**（call by sharing）。多数面向对象语言都采用这一模式，包括 Ruby、Smalltalk 和 Java（Java 的引用类型是这样，基本类型按值传参）。

**共享传参指函数的各个形式参数获得实参中各个引用的副本**。也就是说，**函数内部的形参是实参的别名**。

这种方案的结果是，函数可能会修改作为参数传入的可变对象，但是无法修改那些对象的标识（即不能把一个对象替换成另一个对象）。

```python
def test(a, b):
    a += b
    return a
  
x, y = 1, 2
test(x, y)
# 3
x, y
# (1, 2)

lx, ly = [1,2], [3,4]
test(lx, ly)
# [1, 2, 3, 4]
lx, ly
# ([1, 2, 3, 4], [3, 4])

t1, t2 = (1,2), (3,4)
test(t1, t2)
# (1, 2, 3, 4)
t1, t2
# ((1, 2), (3, 4))
```

###### 不要使用可变类型作为参数的默认值

可选参数可以有默认值，这是 Python 函数定义的一个很棒的特性，这样我们的 API 在进化的同时能保证向后兼容。然而，我们应该避免使用可变的对象作为参数的默认值。

```python
class Bus(object):
    def __init__(self, passengers = []):
        self.passagers = passengers
    def up(self, someone):
        self.passagers.append(someone)
    def down(self, someone):
        self.passagers.remove(someone)
        
bus1 = Bus(['A', 'B'])
bus1.passagers
Out[3]: ['A', 'B']
bus1.up('C')
bus1.down('A')
bus1.passagers
Out[6]: ['B', 'C']
  
bus2 = Bus()
bus2.passagers
Out[8]: []
bus2.up('D')
bus2.passagers
Out[10]: ['D']
  
bus3 = Bus()
bus3.passagers
Out[12]: ['D']
bus3.up('E')
bus2.passagers
Out[14]: ['D', 'E']   # 登上bus3的E在bus2中
  
bus2.passagers is bus3.passagers  # bus2.passagers 和bus3.passagers 指代同一个列表
Out[15]: True
bus1.passagers
Out[16]: ['B', 'C']  # bus1.passagers 是不同的列表
```

问题在于，没有指定初始乘客的 Bus 实例会共享同一个乘客列表。	

实例化 Bus 时，如果传入乘客，会按预期运作。但是不为 Bus 指定乘客的话，奇怪的事就发生了，这是因为 **self.passengers 变成了 passengers 参数默认值的别名**。出现这个问题的根源是，**默认值在定义函数时计算（通常在加载模块时）**，因此**默认值变成了函数对象的属性**。因此，如果默认值是可变对象，而且修改了它的值，那么后续的函数调用都会受到影响。

 审 查`Bus.__init__ `对 象， 看 看 它 的` __defaults__ `属性中的元素：

```python
Bus.__init__.__defaults__
Out[18]: (['D', 'E'],)
```

可以验证 bus2.passengers 是一个别名，它绑定到`Bus.__init__.__defaults__ `属性的第一个元素上：

```python
Bus.__init__.__defaults__[0] is bus2.passagers
Out[19]: True
Bus.__init__.__defaults__[0] is bus3.passagers
Out[20]: True
```

可变默认值导致的这个问题说明了为什么通常使用 None 作为接收可变值的参数的默认值 （我的理解：之前的正确代码是通过 if passengers is None判断 passengers 是否为空，如果为空，通过self.passagers = [] 空列表赋值给self.passagers， 这样就在函数体里面执行，而不是在def定义时执行，空列表也就不会成为函数对象的属性了）。在之前正确的示例中，`__init__ `方法检查 passengers 参数的值是不是 None，如果是就把一个新的空列表赋值给 self.passengers。如果 passengers 不是 None，正确的实现会把 passengers 的副本赋值给 self.passengers。

---

#### 8. 防御可变参数

如果定义的函数接收可变参数，应谨慎考虑调用方是否期望修改传入的参数。

例如，若函数接收一个字典，且在处理的过程中要修改它，那么这个副作用要不要体现到函数外部？应该具体情况具体分析。

```python
class Bus(object):
    def __init__(self, passengers = None):
        if passengers  is None:
            self.passengers  = []
        else:
            self.passengers  = passengers   # 这里不是list(passengers)

    def up(self, someone):
        self.passengers .append(someone)

    def down(self, someone):
        self.passengers .remove(someone)
        
team = ['A', 'B', 'C', 'D']
bus = Bus(team)
bus.passengers 
# ['A', 'B', 'C', 'D']

bus.down('A')
bus.down('B')
bus.passengers 
# ['C', 'D']
team
# ['C', 'D']
```

A、B从bus下车后，team的成员名单竟然也变了！  

Bus 类中`__init__`方法中把 self.passengers 变成 passengers 的别名，而实例化bus后把self.passengers是传给` __init__ `方法的实参的别名team。在 self.passengers 上调用 .remove() 和 .append() 方法其实会修改传给构造方法的那个列表。

这里的问题是: 校车Bus **为传给构造方法的列表创建了别名**。正确的做法是，校车自己只维护乘客列表。修正的方法：在 `__init__` 中，传入 passengers 参数时，应该把参数值的副本赋值给 self.passengers， 比如使用`list(passengers)`。另外，此时传给 passengers 参数的值可以是元组或任何其他可迭代对象，例如set 对象，甚至数据库查询结果，因为 list 构造方法接受任何可迭代对象。自己创建并管理列表可以确保支持所需的 .remove() 和 .append() 操作，这样 .pick() 和 .drop() 方法才能正常运作。

**小结：除非当前方法确实想修改通过参数传入的对象，否则在类中直接把参数赋值给实例变量之前，一定要三思，因为这样会为参数对象创建 别名 。如果不确定，那就创建副本。**

---

#### 9. del和垃圾回收

对象绝不会自行销毁；然而，无法得到对象时，可能会被当作垃圾回收。

**del 语句删除名称，而不是对象**。del 命令可能会导致对象被当作垃圾回收，但是仅当删除的变量保存的是对象的最后一个引用，或者无法得到对象时。重新绑定也可能会导致对象的引用数量归零，导致对象被销毁。

有个` __del__ `特殊方法，但是它不会销毁实例，不应该在代码中调用。即将销毁实例时，Python 解释器会调用 `__del__ `方法，给实例最后的机会，释放外部资源。

在 CPython 中，垃圾回收使用的主要算法是**引用计数**。实际上，每个对象都会统计有多少引用指向自己。当引用计数归零时，对象立即就被销毁：CPython 会在对象上调用 `__del__`方法（如果定义了），然后释放分配给对象的内存。CPython 2.0 增加了分代垃圾回收算法，用于检测引用循环中涉及的对象组——如果一组对象之间全是相互引用，即使再出色的引用方式也会导致组中的对象不可获取。Python 的其他实现有更复杂的垃圾回收程序，而且不依赖引用计数，这意味着，对象的引用数量为零时可能不会立即调用` __del__ `方法。

示例：使用 weakref.finalize 注册一个回调函数，在销毁对象时调用，来演示对象生命结束的情形。

```python
import weakref

s1 = {1,2,3}
s2 = s1    	# s1和s2是别名，指向同一个集合{1, 2, 3}
def bye():   # 这个函数一定不能是要销毁的对象的绑定方法，否则会有一个指向对象的引用。
    print('bye~')  # 在 s1 引用的对象上注册 bye 回调
    
ender = weakref.finalize(s1, bye)  

ender.alive
# True
del s1
ender.alive  # del 不删除对象，而是删除对象的引用。
# True
s2 = 'new s2'
# bye~
# 重新绑定最后一个引用 s2，让 {1, 2, 3} 无法获取。对象被销毁了
# 调用了 bye 回调，ender.alive 的值变成了 False。
```

----

#### 10. 弱引用

正是因为**有引用，对象才会在内存中存在**。当对象的引用数量归零后，垃圾回收程序会把对象销毁。但是，有时需要引用对象，而不让对象存在的时间超过所需时间。这经常用在缓存中。

**弱引用不会增加对象的引用数量**。引用的目标对象称为所指对象（referent）。因此我们说，**弱引用不会妨碍所指对象被当作垃圾回收。**

弱引用在缓存应用中很有用，因为我们不想仅因为被缓存引用着而始终保存缓存对象。

##### WeakValueDictionary简介：

WeakValueDictionary 类实现的是**一种可变映射，里面的值是对象的弱引用**。被引用的对象在程序中的其他地方被当作垃圾回收后，对应的键会自动从 WeakValueDictionary 中删除。因此，WeakValueDictionary 经常用于缓存。

```python
import weakref

class Cheese():
    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return f'Chess-{self.kind}'

stock = weakref.WeakValueDictionary()  # stock 是 WeakValueDictionary 实例。
catalog = [Cheese('Leicester'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Parmesan')]

for cheese in catalog:
    stock[cheese.kind] = cheese  # stock把奶酪的名称映射到catalog中Cheese实例的弱引用上

del catalog
print(sorted(stock.keys()))   # ['Parmesan']

del cheese
print(sorted(stock.keys()))   # []
```

删除 catalog 之后，stock 中的大多数奶酪都不见了，这是 WeakValueDictionary 的预期行为。

`for cheese in catalog`，临时变量cheese引用了对象，这可能会导致该变量的存在时间比预期长。通常，这对局部变量来说不是问题，因为它们在函数返回时会被销毁。但是在示例中，for 循环中的变量 cheese 是全局变量，除非显式删除，否则不会消失。

---

#### 11. 弱引用的局限

不是每个 Python 对象都可以作为弱引用的目标（或称所指对象）。**基本的 list 和 dict 实例不能作为所指对象**，但是它们的子类可以轻松地解决这个问题：

```python
li = range(10)
ref = weakref.ref(li)
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-15-740a7eb0b541>", line 1, in <module>
    ref = weakref.ref(li)
TypeError: cannot create weak reference to 'range' object
  
class Mylist(list):
    pass
myli = Mylist(range(10))
myref = weakref.ref(myli)
```

set 实例可以作为所指对象，因此上面的那个示例才使用 set 实例。用户定义的类型也没问题，这就解释了为什么使用那个简单的 Cheese 类。但是，**int 和 tuple 实例不能作为弱引用的目标，甚至它们的子类也不行。**

---

#### 12. Python对不可变类型施加的把戏

通过前面的学习，我知道对于列表，如列表li，`li[:]`会创建一个副本，而`list(li)`返回一个对象的引用。

```python
li = [1,2,3]

li2 = li[:]  # 创建副本
li is li2
# False

li3 = list(li)  # 创建副本
li3 is li
# False

li4 = li 
li4 is li
# True
```

对元组 t ，`t[:] `不创建副本，而是返回**同一个对象的引用**。此外，`tuple(t)` 获得的也是**同一个元组的引用**。

```python
t = (1,2,3)

t2 = t[:]
t2 is t
# True

t3 = tuple(t)
t3 is t
# True

t4 = t 
t4 is t
# True
```

**str、bytes 和 frozenset 实例也有这种行为**。注意，frozenset 实例不是序列，因此不能使用 `fs[:]`（fs 是一个 frozenset 实例），但是`fs.copy() `具有相同的效果：它会欺骗你，返回同一个对象的引用，而不是创建一个副本。

字符串字面量可能会创建共享的对象：

```python
t = (1,2,3)
t2 = (1,2,3)
t2 is t
# False

l = [1,2,3]
l2 = [1,2,3]
l2 is l
# False

s = 'abc'
s1 = 'abc'
s1 is s
# True
```

**共享字符串字面量是一种优化措施，称为驻留**（interning）。CPython 还会在小的整数上使用这个优化措施，防止重复创建“热门”数字，如 0、—1 和 42。注意，CPython 不会驻留所有字符串和整数，驻留的条件是实现细节，而且没有文档说明。

**千万不要依赖字符串或整数的驻留！比较字符串或整数是否相等时，应该使用 ==，而不是 is。**驻留是 Python 解释器内部使用的一个特性。

---

#### 13. 小结

1. 每个 Python 对象都有**标识**、**类型**和**值**。只有对象的值会不时变化。

2. 如果两个变量指代的 *不可变对象*  具有相同的值（a == b 为 True），实际上它们指代的是副本还是同一个对象的别名基本没什么关系，因为不可变对象的值不会变。但有一个例外：不可变的集合，如 *元组*  和 *frozenset* ：如果不可变集合保存的是可变元素的引用，那么可变元素的值发生变化后，不可变集合也会随之改变。实际上，这种情况不是很常见。不可变集合不变的是所含对象的标识。

3. **变量保存的是引用**，这一点对 Python 编程有很多实际的影响。
   - 简单的赋值不创建副本。
   - 对 += 或 *= 所做的增量赋值来说，如果左边的变量绑定的是不可变对象，会创建新对象；如果是可变对象，会就地修改。
   - 为现有的变量赋予新值，不会修改之前绑定的变量。这叫重新绑定：现在变量绑定了其他对象。如果变量是之前那个对象的最后一个引用，对象会被当作垃圾回收。
   - 函数的参数以别名的形式传递，这意味着，函数可能会修改通过参数传入的可变对象。这一行为无法避免，除非在本地创建副本，或者使用不可变对象（例如，传入元组，而不传入列表）。
   - 使用可变类型作为函数参数的默认值有危险，因为如果就地修改了参数，默认值也就变了，这会影响以后使用默认值的调用。

4. 在 CPython 中，**对象的引用数量归零后，对象会被立即销毁**。如果除了循环引用之外没有其他引用，两个对象都会被销毁。某些情况下，可能需要保存对象的引用，但不留存对象本身。例如，有一个类想要记录所有实例。这个需求可以使用弱引用实现，这是一种低层机制，是 weakref 模块中 WeakValueDictionary、WeakKeyDictionary 和 WeakSet 等有用的集合类，以及 finalize 函数的底层支持。