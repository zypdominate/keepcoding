## 集合set

集合的本质是许多**唯一对象**的聚集。因此，集合可以用于去重。

列表、字典、集合等不可散列的对象是不能用来作为集合的元素的，不可变的对象如字符串、元组等可散列才可以。

```python
set([1,2,3,[4,5]])
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-3-97f17f7a499c>", line 1, in <module>
    set([1,2,3,[4,5]])
TypeError: unhashable type: 'list'
    
set([1,2,3,{'4':5}])
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-5-eae42bf28a0e>", line 1, in <module>
    set([1,2,3,{'4':5}])
TypeError: unhashable type: 'dict'
    
set([1,2,3,{1,2,3}])
Traceback (most recent call last):
  File "D:\Python3.6.0\lib\site-packages\IPython\core\interactiveshell.py", line 2961, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-12-435ddc9ed94f>", line 1, in <module>
    set([1,2,3,{1,2,3}])
TypeError: unhashable type: 'set'
    
set([1,2,3,(4,5)])
Out[4]: {(4, 5), 1, 2, 3}
  
set([1,2,"123"])
Out[5]: {1, '123', 2}
  
item = frozenset([1,2,3])
set([1,2,3,item])
Out[11]: {1, 2, 3, frozenset({1, 2, 3})}
```

```python
li = [1,2,3,4,4]
set(li)
Out[6]: {1, 2, 3, 4}
```

**集合中的元素必须是可散列的，set 类型本身是不可散列的**，但是 frozenset 可以。因此可以创建一个包含不同 frozenset 的 set。 

除了保证唯一性，集合还实现了很多基础的中缀运算符 。给定两个集合 a 和 b，a | b 返回的是它们的合集，a & b 得到的是交集，而 a - b 得到的是差集。合理地利用这些操作，不仅能够让代码的行数变少，还能减少 Python 程序的运行时间。这样做同时也是为了让代码更易读，从而更容易判断程序的正确性，因为利用这些运算符可以省去不必要的循环和逻辑操作。

集合字面量：

除空集之外，集合的字面量——{1}、{1, 2}，等等——看起来跟它的数学形式一模一样。如果是空集，那么必须写成 set() 的形式。如果要创建一个空集，你必须用不带任何参数的构造方法 set()。如果只是写成 {} 的形式，跟以前一样，你创建的其实是个空字典。

集合的推导：

```python
from unicodedata import name
s = {chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')}
s
{'#', '$', '%', '+', '<', '=', '>', '¢', '£', '¤', '¥', '§', '©', '¬', '®', '°', '±', 'µ', '¶', '×', '÷'}
```

---

集合的数学运算：

| 数学符号 | 运算符   | 方法                                   | 描述                                                         |
| -------- | -------- | -------------------------------------- | ------------------------------------------------------------ |
| S ∩ Z    | s & z    | `s.__and__(z) `                        | s和z的交集                                                   |
|          | z & s    | `s.__rand__(z) `                       | 反向 & 操作                                                  |
|          |          | s.intersection(it, ...)                | 把可迭代的 it 和其他所有参数转化为集合，然后求它们与 s 的交集 |
|          | s &= z   | `s.__iand__(z)`                        | 把 s 更新为 s 和 z 的交集                                    |
|          |          | s.intersection_update(it, ...)         | 把可迭代的 it 和其他所有参数转化为集合，然后求得它们与 s 的交集，然后把 s 更新成这个交集 |
| S ∪ Z    | `s | z`  | `s.__or__(z) `                         | s 和 z 的并集                                                |
|          | `z | s`  | `s.__ror__(z) `                        | \|的反向操作                                                 |
|          |          | s.union(it, ...)                       | 把可迭代的 it 和其他所有参数转化为集合，然后求它们和 s 的并集 |
|          | `s |= z` | `s.__ior__(z)`                         | 把 s 更新为 s 和 z 的并集                                    |
|          |          | s.update(it, ...)                      | 把可迭代的 it 和其他所有参数转化为集合，然后求它们和 s 的并集，并把 s 更新成这个并集 |
| S \ Z    | s - z    | `s.__sub__(z)`                         | s 和 z 的差集，或者叫作相对补集                              |
|          | z - s    | `s.__rsub__(z)`                        | - 的反向操作                                                 |
|          |          | s.difference(it, ...)                  | 把可迭代的 it 和其他所有参数转化为集合，然后求它们和 s 的差集 |
|          | s -= z   | `s.__isub__(z)`                        | 把 s 更新为它与 z 的差集                                     |
|          |          | s.difference_update(it, ...)           | 把可迭代的 it 和其他所有参数转化为集合，求它们和 s 的差集，然后把 s 更新成这个差集 |
|          |          | s.symmetric_difference(it)             | 求 s 和 set(it) 的对称差集                                   |
| S ∆ Z    | s ^ z    | `s.__xor__(z)`                         | 求 s 和 z 的对称差集                                         |
|          | z ^ s    | `s.__rxor__(z)`                        | ^ 的反向操作                                                 |
|          |          | s.symmetric_difference_update(it, ...) | 把可迭代的 it 和其他所有参数转化为集合，然后求它们和 s 的对称差集，最后把 s 更新成该结果 |
|          | z ^= s   | `s.__ixor__(z)`                        | 把 s 更新成它与 z 的对称差集                                 |

---

集合的比较运算：

| 数学符号 | 运算符 | 方法                | 描述                                                         |
| -------- | ------ | ------------------- | ------------------------------------------------------------ |
|          |        | s.isdisjoint(z)     | 查看 s 和 z 是否不相交（没有共同元素）                       |
| e ∈ S    | e in s | `s.__contains__(e)` | 元素 e 是否属于 s                                            |
| S ⊆ Z    | s <= z | `s.__le__(z)`       | s 是否为 z 的子集                                            |
|          |        | s.issubset(it)      | 把可迭代的 it 转化为集合，然后查看 s 是否为它的子集          |
| S ⊂ Z    | s < z  | `s.__lt__(z)`       | s 是否为 z 的真子集                                          |
| S ⊇ Z    | s >= z | `s.__ge__(z)`       | s 是否为 z 的父集                                            |
|          |        | s.issuperset(it)    | 把可迭代的 it 转化为集合，然后查看 s 是否为它的父集，然后查看 s 是否为它的父集 |
| S ⊃ Z    | s > z  | `s.__gt__(z)`       | s 是否为 z 的真父集                                          |

---

**散列表**其实是一个**稀疏数组**（总是有空白元素的数组称为稀疏数组）。在一般的数据结构教材中，散列表里的单元通常叫作**表元**（bucket）。在 dict 的散列表当中，每个键值对都占用一个表元，每个表元都有两个部分，一个是对键的引用，另一个是对值的引用。因为所有表元的大小一致，所以可以通过偏移量来读取某个表元。

因为 Python 会设法保证大概还有三分之一的表元是空的，所以在快要达到这个阈值的时候，原有的散列表会被复制到一个更大的空间里面。 如果要把一个对象放入散列表，那么首先要计算这个元素键的散列值。Python 中可以用hash() 方法来做这件事情。

由于**字典使用了散列表**，而散列表又必须是稀疏的，这导致它在空间上的效率低下。如果需要存放数量巨大的记录，那么放在由元组或是具名元组构成的列表中会是比较好的选择；最好不要根据 JSON 的风格，用由字典组成的列表来存放这些记录。**用元组取代字典就能节省空间**的原因有两个：其一是避免了散列表所耗费的空间，其二是无需把记录中字段的名字在每个元素里都存一遍。

set的实现以及导致的结果：

set 和 frozenset 的实现也依赖散列表，但在它们的散列表里存放的只有元素的引用（就像在字典里只存放键而没有相应的值）。在 set 加入到 Python 之前，都是把字典加上无意义的值当作集合来用的。

---

字典和散列表的几个特点，对集合来说几乎都是适用的：

- 集合里的元素必须是可散列的。 

- 集合很消耗内存。 
- 可以很高效地判断元素是否存在于某个集合。 
- 元素的次序取决于被添加到集合里的次序。 
- 往集合里添加元素，可能会改变集合里已有元素的次序。

dict 和 set 背后的散列表效率很高，对它的了解越深入，就越能理解为什么被保存的元素会呈现出不同的顺序，以及已有的元素顺序会发生变化的原因。同时，速度是以牺牲空间为代价而换来的。

