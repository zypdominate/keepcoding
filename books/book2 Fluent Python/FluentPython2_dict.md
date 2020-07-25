#Python数据模型：字典

#### 泛映射类型

dict 类型不但在各种程序里广泛使用，它也是 Python 语言的基石。模块的命名空间、实例的属性和函数的关键字参数中都可以看到字典的身影。跟它有关的内置函数都在`_builtins__.__dict__` 模块中。

大纲：

​	• 常见的字典方法 

​	• 如何处理查找不到的键 

​	• 标准库中 dict 类型的变种 

​	• set 和 frozenset 类型 

​	• 散列表的工作原理 

​	• 散列表带来的潜在影响（什么样的数据类型可作为键、不可预知的顺序，等等）



标准库里的所有映射类型都是利用 dict 来实现的，因此它们有个共同的限制，即**只有可散列的数据类型才能用作这些映射里的键（只有键有这个要求，值并不需要是可散列的数据类型）**。

什么是**可散列的数据类型**:

如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的，而且这个对象需要实现 	`__hash__()` 方法。另外可散列对象还要有`__qe__()`方法，这样才能跟其他键做比较。如果两个可散列对象是相等的，那么它们的散列值一定是一样的……

**原子不可变数据类型（str、bytes 和数值类型）都是可散列类型，frozenset 也是可散列的**，因为根据其定义，frozenset 里只能容纳可散列类型。元组的话，只有当一个元组包含的所有元素都是可散列类型的情况下，它才是可散列的。

```python
tu1 = (1,2,(3,4))
hash(tu1)
Out[3]: -2725224101759650258

tu2 = (1,2,[3,4])
hash(tu2)
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-28-fe78ef742d85>", line 1, in <module>
    hash(tu2)
TypeError: unhashable type: 'list'
    
frozenset1 = frozenset(range(3))
frozenset1
Out[3]: frozenset({0, 1, 2})
tu2 = (1,2,frozenset1)
hash(tu2)
Out[4]: -2745387924187706777
```

字典创建的不同方式：

```python
a = dict(one=1,two=2,three=3)
b = {'one':1,'two':2,'three':3}
c = dict(zip(['one','two','three'],[1,2,3]))
d = dict([('one',1),('two',2),('three',3)])
a == b == c == d
```



#### 字典推导

字典推导（dictcomp）可以从任何以键值对作为元素的可迭代对象中构建出字典。

dict、collections.defaultdict和collections.OrderedDict这三种**映射类型**的方法列表（依然省略了继承自object的常见方法）；可选参数以[...]表示

|                            | dict | defaultdict | OrderedDict |                                                              |
| -------------------------- | :--: | :---------: | :---------: | ------------------------------------------------------------ |
| d.clear()                  |  √   |      √      |      √      | 移除所有元素                                                 |
| `d.__contains__(k)`        |  √   |      √      |      √      | 检查键k是否在d中                                             |
| d.copy()                   |  √   |      √      |      √      | 浅复制                                                       |
| `d.__copy__()`             |      |      √      |             | 用于支持copy.copy                                            |
| d.default_factoy           |      |      √      |             | 在`__missing__`函数中被调用的函数，用以未找到的元素设置值    |
| `d.__delitem__(k)`         |  √   |      √      |      √      | del d[k], 移除键为k的元素                                    |
| d.fromkeys(it, [initial])  |  √   |      √      |      √      | 将迭代器it里的元素设置为映射里的键，若有initial参数，就把它作为这些键对应的值（默认是None） |
| d.get(k, [default])        |  √   |      √      |      √      | 返回键k对应的值，若字典里没有键k，则返回None或default        |
| `d.__getitem__(k)`         |  √   |      √      |      √      | 让字典d能用d[k]的形式返回键k对应的值                         |
| d.items()                  |  √   |      √      |      √      | 返回d里所有对的键值对                                        |
| `d.__iter__()`             |  √   |      √      |      √      | 获取键的迭代器                                               |
| d.keys()                   |  √   |      √      |      √      | 获取所有的键                                                 |
| `d.__len__()`              |  √   |      √      |      √      | 可用len(d)得到字典里键值对的数量                             |
| `d.__missing__(k)`         |      |      √      |             | 当`__getitem__`找不到对应键时被调用                          |
| d.move_to_end(k, [last])   |      |             |      √      | 把键为k的元素移动到最靠前或最靠后的位置（last的默认值为True） |
| d.pop(k, [default])        |  √   |      √      |      √      | 返回键k所对应的值，然后移除这个键值对。若没有这个键，返回None或default |
| d.popitem()                |  √   |      √      |      √      | 随机返回一个键值对，并从字典里移除它                         |
| `d.__reversed__()`         |      |             |      √      | 返回倒序的键的迭代器                                         |
| d.setdefault(k, [default]) |  √   |      √      |      √      | 若字典里有键k，则把它对应的值设置为default，然后返回这个值；若无，则让d[k]=default, 然后返回default |
| `d.__setitem__(k, v)`      |  √   |      √      |      √      | 实现d[k]=v操作，把k对应的值设为v                             |
| d.update(m, [**kargs])     |  √   |      √      |      √      | m可以是映射或键值对迭代器，用来更新d里对应的条目             |
| d.values()                 |  √   |      √      |      √      | 返回字典里的所有值                                           |

注：default_factory 并不是一个方法，而是一个可调用对象（callable），它的值在 defaultdict 初始化的时候由用户设定。 OrderedDict.popitem() 会移除字典里最先插入的元素（先进先出）；同时这个方法还有一个可选的 last 参数，若为真，则会移除最后插入的元素（后进先出）。



#### 用setdefault处理找不到的键

当字典 d[k] 不能找到正确的键的时候，Python 会抛出异常，这个行为符合 Python 所信奉的“快速失败”哲学。可以用 d.get(k, default) 来代替 d[k]， 给找不到的键一个默认的返回值（这比处理 KeyError 要方便不少）。但是要更新某个键对应 的值的时候，不管使用` __getitem__` 还是 get 都会不自然，而且效率低。就像以下示例中的还没有经过优化的代码所显示的那样，dict.get 并不是处理找不到的键的最好方法。

从索引中获取单词出现的频率信息，并把它们写进对应的列表里：

```python
import sys
import re

word_re = re.compile(r'\w+')

index = {}
# with open(sys.argv[1], encoding='utf-8') as f:
with open('test.py', encoding='utf-8') as f:
    for line_index, line in enumerate(f, 1):  # line_index从1开始
        # print(line)
        for match_obj in word_re.finditer(line):
            # print(match_obj)
            word = match_obj.group()
            column_index = match_obj.start() + 1
            location_tup = (line_index, column_index)
            # word_list = index.get(word,[])
            # word_list.append(location_tup)
            # index[word] =word_list

            # 获取单词的出现情况列表，如果单词不存在，把单词和一个空列表放进映射，
            # 然后返回这个空列表，这样就能在不进行第二次查找的情况下更新列表了。
            index.setdefault(word, []).append(location_tup)  # 优化后

# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, index[word])
```

```python
# index.setdefault(word, []).append(location_tup)的效果等价于以下，只不过至少两次键查询：
if word not in index:
  index[word] = []
index[word].append(location_tup)
```

如何单纯地查找取值（而不是通过查找来插入新值）？



#### 映射的弹性键查询





- 通过defaultdict类型，而不是普通的dict
- 自定义一个dict子类，在子类中实现`__missing__`方法

**1. 通过defaultdict类型，而不是普通的dict**

使用**collections.defaultdict**，在用户创建 defaultdict 对象的时候，就需要给它配置一个为找不到的键创造默认值的方法。在实例化一个 defaultdict 的时候，需要给构造方法提供一个可调用对象，这个可调用对象会在 `__getitem__` 碰到找不到的键的时候被调用，让` __getitem__ `返回某种默认值。如果在创建 defaultdict 的时候没有指定 default_factory，查询不存在的键会触发KeyError。

defaultdict 里的 default_factory 只会在` __getitem__ `里被调用，在其他的 方法里完全不会发挥作用。比如，dd 是个 defaultdict，k 是个找不到的键，dd[k] 这个表达式会调用 default_factory 创造某个默认值，而 dd.get(k) 则会返回 None。

```python
import re
import collections

word_re = re.compile(r'\w+')
index_dict = collections.defaultdict(list)  # 把list构造方法作为 default_factory 来创建一个 defaultdict。

with open('test.py', encoding='utf-8') as f:
    for line_index, line in enumerate(f, 1):
        print(line)
        for match_obj in word_re.finditer(line):
            print(match_obj)
            word = match_obj.group()
            column_index = match_obj.start() + 1
            location_tup = (line_index, column_index)
            index_dict[word].append(location_tup)  
            # 若index_dict没有word，则default_factory会被调用，为查询不到的键创造一个值。
            # 这个值在这里是一个空的列表，然后这个空列表被赋值给 index_dict[word]，
            # 继而被当作返回值返回，因此 .append(location_tup) 操作总能成功。
```

**2. 自定义一个dict子类，在子类中实现`__missing__`方法**

```python
# 在查询的时候把非字符串的键转换为字符串

class StrKeyDict(dict):  # 继承dict
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)  # 若找不到的键本身就是字符串，抛出异常
        return self[str(key)]  # 否则，把它转换成字符串再查找

    def get(self, key, default=None):
        # get 方法把查找工作用 self[key] 的形式委托给 __getitem__，
        # 在查找失败前，还能通过 __missing__ 再给某个键通过self[str(key)]查找的机会
        try:
            return self[key]
        except KeyError:  # 若抛出KeyError，说明 __missing__ 也失败了，返回 default。
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()


strDict = StrKeyDict({'one': 1, 2: 2, '3': 'three'})
print(strDict[3])
print(strDict.get(4, 0))
```

为什么 isinstance(key, str) 在上面例子中是必需的。如果没有这个测试，只要 str(k) 返回的是一个存在的键，那么 `__missing__ `方法是没问题的，不管是字符串键还是非字符串键，它都能正常运行。但是如果 str(k) 不是一个存在的键，代码就会陷入无限递归。这是因为 `__missing__` 的最后一行中的 self[str(key)] 会调用` __getitem__`，而这个 str(key) 又不存在，于是` __missing__` 又会被调用。

为了保持一致性，`__contains__ `方法在这里也是必需的。这是因为 `key in dict` 操作会调用它，但是我们从 dict 继承到的` __contains__ `方法不会在找不到键的时候调用 `__missing__`方法。`__contains__` 里还有个细节，就是我们这里没有用更具 Python 风格的方式——k in my_dict——来检查键是否存在，因为那也会导致 `__contains__` 被递归调用。为了避免这一情况，这里采取了更显式的方法，直接在这个 self.keys() 里查询。



#### 字典的变种

标准库里 collections 模块中，除了 defaultdict 之外的不同映射类型：

- collections.OrderedDict

  这个类型在添加键的时候会保持顺序，因此键的迭代次序总是一致的。OrderedDict 的 popitem 方法默认删除并返回的是字典里的最后一个元素，但是如果像 my_odict.popitem(last=False) 这样调用它，那么它删除并返回第一个被添加进去的元素。 

- collections.ChainMap

  该类型可以容纳数个不同的映射对象，然后在进行键查找操作的时候，这些对象会被当作一个整体被逐个查找，直到键被找到为止。

- colllections.Counter

  这个映射类型会给键准备一个整数计数器。每次更新一个键的时候都会增加这个计数器。所以这个类型可以用来给可散列表对象计数，或者是当成多重集来用——多重集合就是集合里的元素可以出现不止一次。Counter 实现了 + 和 - 运算符用来合并记录，还有像 most_common([n]) 这类很有用的方法。most_common([n]) 会按照次序返回映射里最常见的 n 个键和它们的计数

  ```python
  c = collections.Counter('qwerqwewqq')
  c
  Out[3]: Counter({'q': 4, 'w': 3, 'e': 2, 'r': 1})
  c.update('abaaa')
  c
  Out[4]: Counter({'q': 4, 'w': 3, 'e': 2, 'r': 1, 'a': 4, 'b': 1})
  c.most_common(2)
  Out[5]: [('q', 4), ('a', 4)]colllections.UserDict 
  ```

- colllections.UserDict 

  这个类其实就是把标准 dict 用纯 Python 又实现了一遍。跟 OrderedDict、ChainMap 和 Counter 这些开箱即用的类型不同，UserDict 是让用户继承写子类的。



#### 不可变映射类型

标准库里所有的映射类型都是可变的，但有时候你会有这样的需求，比如不能让用户错误地修改某个映射。

从 Python 3.3 开始，types 模块中引入了一个封装类名叫 MappingProxyType。如果给这个类一个映射，它会返回一个**只读的映射视图**。虽然是个只读视图，但是它是**动态**的。这意味着如果对原映射做出了改动，我们通过这个视图可以观察到，但是无法通过这个视图对原映射做出修改。

```python
from types import MappingProxyType

adict = {1:'A', 2:'B'}
adict_proxy = MappingProxyType(adict)
adict_proxy
Out[3]: mappingproxy({1: 'A', 2: 'B'})
  
adict_proxy[1]
Out[4]: 'A'
adict_proxy[2]
Out[5]: 'B'
adict_proxy[2] = "c"
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-145-372f87dbe97b>", line 1, in <module>
    adict_proxy[2] = "c"
TypeError: 'mappingproxy' object does not support item assignment
  
adict[2] = 'C'
adict_proxy
Out[6]: mappingproxy({1: 'A', 2: 'C'})
adict_proxy[2]
Out[7]: 'C'
```



####  dict的实现及导致的结果

dict的实现及其导致的结果:

1. 键必须是可散列的 

一个可散列的对象必须满足以下要求。 

- 支持 hash() 函数，并且通过` __hash__()` 方法所得到的散列值是不变的。 
-  支持通过` __eq__() `方法来检测相等性。 
-  若 a == b 为真，则 hash(a) == hash(b) 也为真。

如果实现了一个类的 `__eq__` 方法，并且希望它是可散列的，那么它一定要有个恰当的 `__hash__ `方法，保证在 a == b 为真的情况下 hash(a) == hash(b) 也必定为真。否则就会破坏恒定的散列表算法，导致由这些对象所组成的字典和集合完全失去可靠性，这个后果是非常可怕的。另一方面，如果一个含有自定义的 `__eq__` 依赖的类处于可变的状态，那就不要在这个类中实现 `__hash__` 方法，因为它的实例是不可散列的。

2. 字典在内存上的开销巨大

由于字典使用了散列表，而散列表又必须是稀疏的，这导致它在空间上的效率低下。

如果需要存放数量巨大的记录，那么放在由元组或是具名元组构成的列表中会是比较好的选择；最好不要根据 JSON 的风格，用由字典组成的列表来存放这些记录。用元组取代字典就能节省空间的原因有两个：其一是避免了散列表所耗费的空间，其二是无需把记录中字段的名字在每个元素里都存一遍。

3. 键查询很快

dict 的实现是典型的空间换时间：字典类型有着巨大的内存开销，但它们提供了无视数据量大小的快速访问——只要字典能被装在内存里。

4.  键的次序取决于添加顺序

当往 dict 里添加新键而又发生散列冲突的时候，新键可能会被安排存放到另一个位置。于是下面这种情况就会发生：由 dict([key1, value1), (key2, value2)] 和 dict([key2, value2], [key1, value1]) 得到的两个字典，在进行比较的时候，它们是相等的；但是如果在 key1 和 key2 被添加到字典里的过程中有冲突发生的话，这两个键出现在字典里的顺序是不一样的。

5. 往字典里添加新键可能会改变已有键的顺序

无论何时往字典里添加新的键，Python 解释器都可能做出为字典扩容的决定。扩容导致的结果就是要新建一个更大的散列表，并把字典里已有的元素添加到新表里。如果在迭代一个字典的所有键的过程中同时对字典进行修改，那么这个循环很有可能会跳过一些键——甚至是跳过那些字典中已经有的键。

因此，不要对字典同时进行迭代和修改。如果想扫描并修改一个字典，最好分成两步来进行：首先对字典迭代，以得出需要添加的内容，把这些内容放在一个新字典里；迭代结束之后再对原有字典进行更新。