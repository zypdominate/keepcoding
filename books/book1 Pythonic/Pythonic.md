Rome was not built in one day， coding will not advance vigorously with one effort.

从量变到智变的飞跃，需要从多方面一点一滴的积累，比如语言层面的使用技巧、常见注意事项、编程风格等。

## 绪

```python
# 快排
# 使用极简代码完成，且易读易理解
def quickSort(array):
    less, more = [], []
    if len(array) <= 1:
        return array
    middle = array.pop()
    for i in array:
        if i < middle:
            less.append(i)
        else:
            more.append(i)
    return quickSort(less) + [middle] + quickSort(more)

testArray = [2,1,6,3,9,8]
print(quickSort(testArray))
```

```python
# 交换两数
# 不像C语言需要找中间变量来传递
a, b = b, a
```

```python
# 迭代器
for i in onelist:
	do_something(i)
```

```python
# 安全地关闭文件：with
with open(onepath, 'r') as f:
	do_something(f)
```

```python
# slice
alist = [1,2,3,4]
newlist = alist[::-1] # 倒序
```

```python
# 字符串格式化
print("newlist %s" % newlist)
# newlist [4, 3, 2, 1]

print("newlist {0}, {1}".format(alist, newlist))
# newlist [1, 2, 3, 4], [4, 3, 2, 1]

print(f"newlist:{newlist}")  # 建议使用f
# 'newlist:[4, 3, 2, 1]'
```

```python
包和模块的命名采用小写、单数形式，且短小
包通常仅作为命名空间，如只包含空 __init__.py 文件
```



## Pythonic的代码

#### 1. 避免劣化代码

- 避免只用大小写区分不同的对象
- 避免使用容易引起混淆的名称
  - 重复使用存在于上下文中的变量名来表示不同的类型
  - 使用内建名称来表示其他含义变量
  - 使用类似于element、list、dict、tuple等来作为变量名
  - 使用o（容易与0混淆），l（容易与数字1混淆）作为变量名
- 不要怕变量名过长
  - 考虑代码的易读和理解，变量名需要长一些

#### 2. 深入认识python

- 全面掌握python提供的特性：语言特性和库特性，参考官方手册Language Reference 和Library Reference。
- 紧跟Python的迭代，学习新知识、新用法等。
  - 深入学习公认的比较pythonic的代码，比如Flask、gevent、requests等
- PEP8：代码布局、注释、命名规范。
  - Pylint、Google Python Style Guide、Pychecker、Pyflakes



## 理解Python与C语言的不同

1. 缩进 vs {}

C、C++、Java等用花括号{}来分隔代码。Python使用严格的代码缩进，空格和Tab不能混用。

2. '' vs ""

C中单引号和双引号有着严格的区别，单引号表示一个字符，对应编译器所采用的字符集中的一个整数值，例如'a'与97对应。双引号表示字符串，默认以'\0'结尾。

在Python中单引号和双引号没有明显的区别，仅在输入字符串内容不同时，存在微小差异。

3. 三元操作符

三元操作符是if...else...的简写方法，语法形式C？X:Y，表示满足满足条件C时取值X否则取值。

4. switch...case

Python中没有switch...case分支语句

```C
switch(n){
  case 0:
    printf("zero \n");
    break;
  case 1:
    printf("one \n");
  default:
    printf("other value \n");
    break;
}
```

```python
if n == 0:
  print("zero")
elif n == 1:
  print("one")
else:
  print("other value")
  
# 或者使用跳转表实现
def func(n):
  return {0:"zero", 1:"one"}.get(n, "other value")
```



## 适当、必要的注释

Python的注释：块注释、行注释、文档注释（docstring）

- 使用块或行注释，仅仅注释那些复杂的操作、算法、别人难以理解的技巧、不熟悉的业务
- 注释和代码隔开一定的距离，可以使用PEP8规范格式化代码
- 给外部可访问的函数和方法添加文档注释。
  - 注释描述方法的功能，对入参、返回值以及可能的异常说明
- 文件头部推荐使用copyright声明、模块描述，添加作者信息及时间
- 注释和代码不能重复，注释是用来解释代码的功能、原因、思路的
- 用于调试的代码等不需要的代码不应该注释，而是应该删除



## 适当空行优雅代码布局

布局清晰、整洁、优雅的代码能够让阅读者比较愉悦。

- 在一组代码表达完一个完整的思路后，应该用空白进行间隔
  - 函数与函数之间、导入声明与变量赋值之间等，无关的代码块之间最好用空行隔开
- 避免过长的代码行，Pycharm：Ctrl+Alt++L格式化
- 逗号前不要用空格



##  函数编写的原则

函数的作用：最大化的代码重用、最小化的代码冗余；
编写函数追求：提高程序的健壮性、增强可读性、减少维护成本。

- 函数设计要尽量短小，嵌套层次浅
  - 避免过长的函数体，在一个屏幕下就能看完整
  - if、elif、for、while嵌套不超过3层
- 函数声明应该合理、简单、易于使用
  - 函数名的见名知意
  - 参数设计简洁明了，入参个数不宜过多
- 函数参数设计应该考虑向下兼容
  - 添加默认参数，适应函数调用接口的变化
- 一个函数只做一件事，尽量避免函数语句粒度的一致性
  - 一个功能可以分解成多个小任务、函数



## 常量集中到一个文件中

Python实际内建命名空间支持一小部分常量：True、False、None等，没有提供定义常量的直接方式。在Python中一般这样使用常量：

- 通过命风格表示该变量为常量：大写，一种约定俗成的风格
- 自定义的类实现常量功能：
  - 命名全部为大写
  - 值一旦绑定就不能修改，否则抛出异常

```python
# constant.py
class Constant(object):
    class ConstError(TypeError):pass
    class ConstCaseError(ConstError):pass
    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError(f"Cant't change constant {key}")
        if not key.isupper():
            raise self.ConstCaseError(f"constant {key} is not all uppercase")
        self.__dict__[key] = value

import sys
sys.modules[__name__] = Constant

# 定义好类后，在其他脚本中使用只要导入上面这个模块就行
# other.py
import constant  # 导入定义常量类的模块
constant.MYNAME = "justme"
```

```
使用sys.modules[__name__]可以获取一个模块对象<module '__main__'>，并可以通过该对象获取模块的属性，这里使用了sys.modules向系统字典中注入了一个Constant对象从而实现了在执行import constant时实际获取了一个Constant实例的功能。	

sys.modules[__name__] = Constant将系统已加载的模块列表中的constant替换为了Constant, 即一个Constant实例。

备注：
sys.modules 是存放已经缓存的模块，值为dict类型
sys.path  搜索路径，值为list类型
if __name__= __main__ 是python的程序入口，如果直接执行该.py文件，那么执行后面的代码，如果作为模块导入，则不执行后面的代码
```

