**`Rome was not built in one day， coding will not advance vigorously with one effort.**

## 字符串的基本用法

Python遇到未闭合的小括号时会自动将多行代码拼接为一行，把相邻的两个字符串变量拼接在一起。

```python
s = ('I '
     'am '
     'coding '
     'step by step')
s
Out[7]: 'I am coding step by step'
```

```
# 字符串的方法（偏僻的方法用到时再去搜索学一下）
'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill'
```



## sort() 和sorted()

```
sorted(iterable[, cmp[, key[, reverse]]])
s.sort([cmp[, key[, reverse]]])
```

- cmp为用户定义的任何比较函数，函数的参数为两个可比较的元素（来自iterable），函数根据第一个参数与第二个参数的关系依次返回 -1、0或者+1（第一个参数小于第二个参数则返回负数）。cmp默认为None。
- key是带一个参数的函数，用来为每个元素提取比较值，默认为None（即直接比较每个元素）
- reverse表示排序结果是否反转

sorted()作用于任意可迭代的对象，而sort()一般作用于列表。

sorted()函数返回一个排序后的列表，原有列表保持不变；而sort()函数会直接修改原有列表，函数返回为None。

**sorted** 的使用：

- 对字典排序

```Python Console
from operator import itemgetter
# 对字典排序
bookowner = {'Bob':'2','Caly':'1','Amy':'3'}

ret_sorted = sorted(bookowner.items(),key=itemgetter(1))
ret_sorted
Out[1]: [('Caly', '1'), ('Bob', '2'), ('Amy', '3')]
  
ret_sorted = sorted(bookowner.items(),key=itemgetter(0))
ret_sorted
Out[2]: [('Amy', '3'), ('Bob', '2'), ('Caly', '1')]
```

- 多维list排序

```python
info = [['Bob', 95, 'A'], ['Caly', 86, 'C'], ['justin', 82, 'A'], ['Amy', 86, 'D']]
sorted(info, key=itemgetter(2, 1))
# Out[3]: [['justin', 82, 'A'], ['Bob', 95, 'A'], ['Caly', 86, 'C'], ['Amy', 86, 'D']]
```

- 字典中混合list排序

```python
mydict = {
    'Bob': ['M', 7],
    'Caly': ['E', 2],
    'Justin': ['P', 3],
    'Amy': ['C', 6]
}
sorted(mydict.items(), key=lambda elem: itemgetter(1)(elem[1]))
```

- list中混合字典排序

```python
ratelist = [
    {'name':'Bob','win':10,'loss':3,'rate':75},
    {'name':'David','win':3,'loss':5,'rate':57},
    {'name':'Carol','win':4,'loss':5,'rate':57},
    {'name':'Patty','win':9,'loss':3,'rate':71},
]
sorted(ratelist,key=itemgetter('rate','name'))
# Out[62]: 
# [{'name': 'Carol', 'win': 4, 'loss': 5, 'rate': 57},
#  {'name': 'David', 'win': 3, 'loss': 5, 'rate': 57},
#  {'name': 'Patty', 'win': 9, 'loss': 3, 'rate': 71},
#  {'name': 'Bob', 'win': 10, 'loss': 3, 'rate': 75}]
```



##  Counter

```python
# 统计次数
# 1、使用dict
data = ['a', '2', 'c', 1, 2, 'a', 'c', 'a', 'b', 0, 1]
count_dict = dict()
for ele in data:
    if ele in count_dict:
        count_dict[ele] +=1
    else:
        count_dict[ele] = 1
# count_dict
# Out[1]: {'a': 3, '2': 1, 'c': 2, 1: 2, 2: 1, 'b': 1, 0: 1}


# 2、使用defaultdict
from collections import defaultdict
count_default = defaultdict(int)
for ele in data:
    count_default[ele] +=1
# count_default
# Out[2]: defaultdict(int, {'a': 3, '2': 1, 'c': 2, 1: 2, 2: 1, 'b': 1, 0: 1})


# 3、使用set和list
count_set = set(data)
count_list = []
for ele in count_set:
    count_list.append((ele, data.count(ele)))
# count_list
# Out[3]: [(0, 1), (1, 2), ('2', 1), (2, 1), ('c', 2), ('b', 1), ('a', 3)]


# 4、更加优雅、简介的方式：使用collection.Counter
# Counter类属于字典类的子类，是一个容器对象，主要用来统计散列对象
# 支持集合操作+-&|，其中&|分别返回两个Counter对象元素的最小值和最大值
from collections import Counter
# 三种方式初始化：可迭代对象、关键字参数、字典
Counter('success')      # Counter({'s': 3, 'u': 1, 'c': 2, 'e': 1})
Counter(a=1, b=2, c=3)      # Counter({'a': 1, 'b': 2, 'c': 3})
Counter({'a': '2', 'c': 1, 2: 'a'})  # Out[8]: Counter({'a': '2', 'c': 1, 2: 'a'})
```

```python
# 使用element()方法来获取Counter中的key值
data = ['a', '2', 'c', 1, 2, 'a', 'c', 'a', 'b', 0, 1]
list(Counter(data).elements())
# Out[10]: ['a', 'a', 'a', '2', 'c', 'c', 1, 1, 2, 'b', 0]

# 使用most_common()方法找出前n个出现频率最高的元素、对应次数
Counter(data).most_common(2)
# Out[12]: [('a', 3), ('c', 2)]

# 当访问的元素不存在时，默认返回0，而不是抛出异常
(Counter(data)['y'])
# Out[13]: 0

# updata()方法用于被统计对象元素的更新，原有Counter计数器对象和新增元素的统计数值相加而不是直接替换它们
c = Counter('success')
# c
# Out[15]: Counter({'s': 3, 'u': 1, 'c': 2, 'e': 1})
c.update('successfully')
# c
# Out[17]: Counter({'s': 6, 'u': 3, 'c': 4, 'e': 2, 'f': 1, 'l': 2, 'y': 1})

# subtract()用于实现计数器对象中元素统计值相减，输入和输出的统计值允许为0或者为负数
c.subtract('successfully')
# c
# Out[19]: Counter({'s': 3, 'u': 1, 'c': 2, 'e': 1, 'f': 0, 'l': 0, 'y': 0})
```



## ConfigParser

配置文件的意义在于用户不需要修改代码，就可以改变应用的行为。

getboolean()函数，根据一定的规则将配置项的值转换为布尔值。

```python
[section1]
option1=0
```

当调用getboolean('section1','option1')) 时，返回False，除了0之外，no、false、off都会被转义为False，对应的1、yes、true、on都会被转义为True，其他值都会导致抛出ValueError异常。

配置项的查找规则，在ConfigParser支持的配置文件格式里，有一个[DEFAULT]节点，当读取的配置项不在指定的节点里时，ConfigParser将会到[DEFAULT]节点中区找。

```python
[section1]
option1=false

[section2]

[DEFAULT]
in_default = 'an option value in default'
```

```python
import configparser
conf = configparser.ConfigParser()
conf.read('example.conf')
print(conf.getboolean('section1','option1'))  # False
print(conf.get('section2','in_default'))    # 'an option value in default'
```

配置项值的查找规则：

1. 若找不到节点名，就抛出NoSectionError；
2. 若给定的配置项出现在get()方法的vars参数中，则返回vars参数中的值；
3. 若在指定的节点中含有给定的配置项，则返回其值；
4. 若在[DEFAULT]中有指定的配置项，则返回其值；
5. 若在构造函数的default参数中有指定的配置项，则返回其值；
6. 抛出NoOptionError；



ConfigParser支持字符串格式化的语法：

```python
example_str = '%(protocol)s://%(server)s:%(port)s/' % {'protocol':'http','server':'example.com','port':1080,}
# http://example.com:1080/
```

```python
[DEFAULT]
conn_str = %(dbn)s://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s
dbn = mysql
user = root
host = localhost
port = 3306

[db1]
user = zyp
pw = ppp
db = example

[db2]
host = 192.168.0.110
pw = www
db =example
```

```python
import configparser
conf = configparser.ConfigParser()
conf.read('example.conf')

print(conf.get('db1','conn_str'))
print(conf.get('db2','conn_str'))
# mysql://zyp:ppp@localhost:3306/example
# mysql://root:www@192.168.0.110:3306/example
```



## pickle

序列化是把内存中的数据结构在不丢失其身份和类型信息的情况下转成对象的文本或二进制的过程。对象序列化后的形式经过饭序列化能恢复为原有对象。Python中有很多支持序列化的模块，如pickle、json、marshal、shelve。

pickle是最通用的序列化模块，还有用C语言实现的cPickle，拥有这更好的性能。

pickle最主要的两个函数：dump()、load()，用于对象的序列化和反序列化。

- pickle.dump(obj, file[,protocol])：序列化数据到一个文件描述符（一个打开的文件、套接字等）。参数obj表示需要序列化的对象，包括布尔、数字、字符串、字节数组、None、列表、元组、字典、集合等基本数据类型，还可以处理循环，递归引用对象、类、函数以及类的实例等。参数file支持write()方法的文件句柄，可以为真实的文件，也可以是StringIO对象。protocol为序列化使用的协议版本，0表示ASCII协议（默认为0），所序列化的对象使用可打印的ASCII码表示；1表示老式的二进制协议；2表示2.3版本引入的新二进制协议，比以前的高效。
- load(file)：表示把文件中的对象恢复为原来的对象（反序列化）

```python
import pickle
data = {'Bob': '2', 'Caly': '1', 'Amy': '3'}

file_name = 'test_pickle.txt'
with open(file_name,'wb') as fp:
    pickle.dump(data, fp)

with open(file_name,'rb') as fp:
    res = pickle.load(fp)
    print(res)
```

pickle的特点：

- 接口简单，容易使用，通过dump和load可以轻松实现序列化和反序列化

- pickle的存储格式具有通用性，能被不同平台的Python解析器共享：Linux下序列化的格式文件可在Windows的Python解析器中反序列化，兼容性好

- 支持的数据类型广泛: 数字、布尔值、字符串，只包含可序列化对象的元组、字典、列表等，非嵌套的函数、类以及通过类的`__dict__`或者`__getstate__`可以返回序列化对象的实例等

- pickle模块是可扩展的。pickle模块是可以扩展的。对于实例对象，pickle在还原对象的时候一般是不调用`__init__()`函数的，如果要调用`__init__()`进行初始化，对于古典类可以在类定义中提供`__getinitargs__()`函数，并返回一个元组，当进行unpickle的时候，Python就会自动调用`__init__()`，并把`__getinitargs__()`中返回的元组作为参数传递给`__init__()`，而对于新式类，可以提供`__getnewargs__()`来提供对象生成时候的参数，在unpickle的时候以`Class.__new__(Class, *arg)`的方

  式创建对象。对于不可序列化的对象，如sockets、文件句柄、数据库连接等，也可以通过实现pickle协议来解决这些局限，主要是通过特殊方法`__getstate__()`和`__setstate__()`来返回实例在被pickle时的状态，见如下示例：

```python
import pickle

class TextReader():
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename)  # 打开文件的句柄
        self.position = self.file.tell()

    def readline(self):
        line = self.file.readline()
        self.position = self.file.tell()
        if not line:
            return None
        if line.endswith('\n'):
            line = line[:-1]
        return f"{self.position}", line

    def __getstate__(self):  # 记录文件被pickle时的状态
        print("in __getstate__")
        state = self.__dict__.copy()  # 获取被pickle时的字典信息
        del state['file']
        return state

    def __setstate__(self, state):  # 设置反序列化后的状态
        print("in __setstate__")
        self.__dict__.update(state)
        file = open(self.filename)
        self.file = file


reader = TextReader("test.py")
print(reader.readline())
print(reader.readline())
print("---")

s = pickle.dumps(reader)  # 在dumps时会默认调用__getstate__
new_reader = pickle.loads(s)  # 在loads时会默认调用__setstate__
print("***")
print(new_reader.readline())
print(new_reader.readline())

```

- 能够自动维护对象间的引用，如果一个对象上存在多个引用，pickle后不会改变对象间的引用，并且能够自动处理循环和递归。



```python
import pickle

a = [1,2]
b = a
b.append(3)

p = pickle.dumps((a,b))
a1, b1 = pickle.loads(p)
a1
Out[1]: [1, 2, 3]
b1
Out[2]: [1, 2, 3]
a1.append(4)
b1
Out[3]: [1, 2, 3, 4]  # 反序列化对a1对象的修改仍然会影响到b1
```

pickle的使用也存在以下限制：

- 不能保证操作的原子性
- 存在安全性问题
- pickle协议是Python特定的，不同语言之间的兼容性难以保障



## json

json是一种轻量级数据交换格式，基于JavaScript的一个子集，可读性和互操作性较强，易于解析和使用。json和pickle类似，使用dump/dumps来序列化，load/loads来反序列化。

json的两大数据结构：名称/值对的集合、值的有序列表

![1570266733734](../../zypictures/books/json文档分解图.png)

​	

## traceback 获取栈信息

tracebac模块可以在发生异常时展示出现场信息，输出完整的栈信息，包括调用顺序、异常发生的语句、错误类型。

traceback.print_exc()方法打印出的信息包括3部分：错误类型(IndexError)、错误对应的值(list index out of range)、具体的trace信息，包括文件名、具体的行号、函数名以及对应的源代码。常用的几个方法：

- traceback.print_exception(type, value, traceback[, limit[, file]])，根据limit的设置打印栈信息，file为None时定位到sys.stderr，否则写入文件；type、value、traceback这3个参数对应的值可以从sys.exc_info()中获取
- traceback.print_exc([limit[, file]])，为print_exception()函数的缩写，不需要传入type、value、traceback
- traceback.format_exc([limit])，与print_exc类似，区别在于返回形式为字符串
- traceback.extract_stack([file, [, [limit]]])，从当前栈帧中提取trace信息



## threading

Python为多线程编提供了模块：thread、threading。

- thread模块提供了多线程底层支持模块，以敌机原始的方式来处理和控制线程，使用较为复杂
- threading模块基于thread进行包装，将线程的操作对象化，在语言层面提供了丰富的特性

一般Python多线程支持两种方式来创建线程：一种是通过继承Thread类，重写它的run()方法；另一种是创建一个threading.Thread对象，在它的初始化函数(`__init__`)中将可调用对象作为参数传入。

[csdn博客：多线程原理及实现](https://blog.csdn.net/qq_31362767/article/details/87538380)



