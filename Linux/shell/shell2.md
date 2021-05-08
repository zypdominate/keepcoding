## 函数的使用

```shell
function hello()
{
    echo "Hello SHell.";
	  return 1;
}
echo "method begin..."
hello
echo "method end..."

# method begin...
# Hello SHell.
# method end...
```

在 Shell 中，参数返回可以显示加 return 返回。如果不加，将以最后一条命令运行结果，作为返回值。返回值只能正整数，并且范围在 0 - 255。

#### 函数参数

在Shell中，调用函数时可以向其传递参数。在函数体内部，通过  \$n 的形式来获取参数的值，例如，$1表示第一个参数，$2表示第二个参数…

```shell
funWithParam(){
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
    echo "第十个参数为 ${10} !"
    echo "第十一个参数为 ${11} !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}
funWithParam 1 2 3 4 5 6 7 8 9 34 73

```

输出结果:

```
第一个参数为 1 !
第二个参数为 2 !
第十个参数为 10 !
第十个参数为 34 !
第十一个参数为 73 !
参数总数有 11 个!
作为一个字符串输出所有参数 1 2 3 4 5 6 7 8 9 34 73 !
```

注意，$10 不能获取第十个参数，获取第十个参数需要${10}。当n>=10时，需要使用${n}来获取参数。

## 输出的重定向

在写 Shell 脚本的时候，我们经常会想将命令的输出结果保存到文件中，或者将命令的执行结果保存到日志记录中。这时候就需要把命令的输出结果重定向。而要进行重定向，就要了解 Linux 的输入输出流。

在 Linux 中有三个经常用到的输入输出流，他们分别是：

* 标准输入（stdin）
* 标准输出（stdout）
* 标准错误（stderr）

在 Linux 系统中，系统保留了 0（标准输入）、1（标准输出）、2（标准错误） 三个文件描述符分别代表它们。

**标准输入指的是从键盘这些标准输入设备读取到的数据。**一般情况下标准输入重定向的很少用到.

**标准输出则是通过屏幕输出的这些数据。**我们可以通过标准输出重定向来让数据保存到文件里。

```shell
$ echo "hello shell" > out.txt
$ cat out.txt
hello shell
# echo 命令的输出并没有在屏幕上打印，而是保存在了out.txt文件中。
```

其实上面这种方式和`echo "hello" 1> out.txt`这条命令的结果是一样的。或许是因为标准输出重定向比较频繁，所以就把数字 1 省略了。

**标准错误是指输出的错误信息。**例如当我们运行一条错误的指令时，控制台会提示凑无信息，这些就是错误信息。如果我们要重定向错误信息到文件中，我们可以用`2>`这个操作符。

```shell
$ ls +
ls: +: No such file or directory
$ ls + 2> error.txt
$ cat error.txt
ls: +: No such file or directory

# 通过2>这个操作符，我们将标准错误重定向到了 error.txt 文件中了。
```

## 文件判断

文件测试运算符用于检测文件的各种状态和属性，目前支持的运算符如下：

* `-b file`：是否块设备文件
* `-c file`：是否字符设别文件
* `-d file`：是否目录
* `-f file`：是否普通文件
* `-g file`：文件是否设置了 SGID 位
* `-k file`：是否设置了粘着位
* `-p file`：文件是否有名管道
* `-u file`：文件是否设置了 SUID 位
* `-r file`：文件是否**可读**
* `-w file`：文件是否**可写**
* `-x file`：文件是否**可执行**
* `-s file`：文件是否为空（文件大小是否大于0），不为空返回 true。
* `-e file`：文件（包括目录）是否存在

要特别注意的是`-s file`判断文件是否为空时，不为空才返回true。

变量 file 表示文件 `/User/hello.sh`，它的大小为 52 字节，具有 rwx 权限。下面的代码，将检测该文件的各种属性：

```shell
#!/bin/bash

file="/User/hello.sh"
if [ -r $file ]
then
   echo "文件可读"
else
   echo "文件不可读"
fi
if [ -w $file ]
then
   echo "文件可写"
else
   echo "文件不可写"
fi
if [ -x $file ]
then
   echo "文件可执行"
else
   echo "文件不可执行"
fi
if [ -f $file ]
then
   echo "文件为普通文件"
else
   echo "文件为特殊文件"
fi
if [ -d $file ]
then
   echo "文件是个目录"
else
   echo "文件不是个目录"
fi
if [ -s $file ]
then
   echo "文件不为空"
else
   echo "文件为空"
fi
if [ -e $file ]
then
   echo "文件存在"
else
   echo "文件不存在"
fi
```

## 算术运算符

在 Shell 中，利用 expr 命令再加上算术运算符可以实现数值运算。目前支持的算术运算符有：

* `+`：加法
* `-`：减法
* `*`：乘法
* `/`：除法
* `%`：取余
* `=`：赋值
* `==`：相等
* `!=`：不相等

在 原生 Bash 不支持简单的数学运算，所以在 Shell 语言中的运算都是通过其他命令来实现的，其中最常用的就是 expr 命令。

```shell
#!/bin/sh
val=`expr 2 + 2`
echo "Total value : $val"
# Total value : 4
```

上面的 ` 符号叫做反引号，作用是将符号内的命令结果赋值给左边的变量。

## 数组

Shell 中有数组这个概念，数组中可以存放多个值。但 Shell 只支持一维数组，不支持多维数组，初始化时不需要定义数组大小。与大部分编程语言类似，数组元素的下标由0开始。

Shell 数组用括号来表示，元素用「空格」符号分割开，语法格式如下：

```shell
array_name=(value1 value2 ... valuen)
```

```shell
#!/bin/bash
my_array=(A B "C" D)
```

也可以使用下标来定义数组：

```shell
array_name[0]=value0
array_name[1]=value1
array_name[2]=value2
```

读取数组元素值的一般格式是：`${array_name[index]}`

```shell
#!/bin/bash
my_array=(A B "C" D)
echo "第一个元素为: ${my_array[0]}"
echo "第二个元素为: ${my_array[1]}"
echo "第三个元素为: ${my_array[2]}"
echo "第四个元素为: ${my_array[3]}"
```

结果:

```shell
$ chmod +x test.sh 
$ ./test.sh
第一个元素为: A
第二个元素为: B
第三个元素为: C
第四个元素为: D
```

获取数组中的所有元素 使用@ 或 * 可以获取数组中的所有元素

```shell
#!/bin/bash

my_array[0]=A
my_array[1]=B
my_array[2]=C
my_array[3]=D

echo "数组的元素为: ${my_array[*]}"
echo "数组的元素为: ${my_array[@]}"
echo "数组元素个数: ${#my_array[*]}"
echo "数组元素个数: ${#my_array[@]}"
```

结果:

```shell
$ chmod +x test.sh 
$ ./test.sh
数组的元素为: A B C D
数组的元素为: A B C D
数组元素个数: 4
数组元素个数: 4
```

## 特殊符号[]、[[]]、(())、$(())、()

括号和括号组成的特殊标识，例如：`[]`、`[[]]`、`(())`、`$(())`、`()`

####test命令

```shell
test {EXPRESSION}
```

```shell
if test "a" == "a"
then 
	echo match!
fi
```

#### []

 [] 符号的作用与 test 命令一样，都用于判断表达式的真假。只不过 [] 将表达式括起来了，更加易读。上面的例子用 [] 重写就会变成这样：

```shell
if [ "a" == "a" ]
then 
	echo match!	
fi
```

```shell
if [ $a -gt 10 -a $a -lt 15 ]
then 
	echo match!	
fi
```

#### [[]]

`[[]]` 符号与 `[]` 符号的区别是，在 `[[]]` 符号里，我们引用变量时可以不再用 $ 符号了，而且还可以使用 && 和 || 运算符。

像上面判断变量 a 的范围，我们在 `[]` 符号中，只能使用 `-gt` 、`-a`、`-lt`等操作符。但如果用`[[]]`实现，我们就可以用上`&&`和`||`操作符：

```shell
a=12
if [[ a -gt 10 && a -lt 15 ]]
then 
	echo match!	
fi
```

#### let命令

```shell
a=10
let b=a+10
echo $b
```

在 let 命令中的变量，不需要使用 \$ 符号就可以使用。像上面的 a 变量，其实一个变量，但是在第 2 行的 let 语句不需要使用 \$ 符号也能成功运算。

#### (())

这组符号的作用与 let 指令相似，用在算数运算上，是 bash 的内建功能。所以，在执行效率上会比使用 let指令要好许多。在这个符号里，我们可以进行整数运算，它的作用和 let 命令一样。

```shell
a=10
(( b = a + 10 ))
echo $b
```

或者我们可以将计算结果作为表达式，如果结果是 0 表示假，其余全部是真。

```shell
a=10
if (( a + 10 ))
then
	echo true
fi
```

```shell
a=10
if (( a <= 12 && a > 0))
then 
  echo great than 10
fi
```

####$(())

和上面的差不多，但是不会像命令一样有返回值，而是会像变量一样把运算结果替换出来。

```shell
a=10
b=$(( a <= 12 && a > 0))
echo $b
```

输出：`1`

```shell
a=10
b=$(( a <= 12 && a < 0))
echo $b
```

输出：`0`

因此如果要让它作为一个表达式的话，就要结合 `[]` 符号。例如：

```shell
a=10
if [ $(( a <= 12 && a > 0)) -eq 1 ]
then 
  echo great than 10
fi
```

对于 `(())` 符号而言只有 bash 这个 Shell 有，而 `$(())` 则是所有 Shell 都有，更为通用。

####()

`()` 符号表示括号中作为一个子 Shell 运行，运行结果不干扰外层的 Shell。

```shell
a=2
(a=1)
echo $a
```

输出是：`2`

因为括号括起来是一个子 Shell，不影响外层 Shell 的运行，所以对 a 赋值为 1 不影响外层结果，外层的 a 变量还是 2。

利用上面子 Shell 这个特性，我们在写 Shell 脚本的时候可以做到不切换当前目录而在其他目录干点事儿。例如：

```shell
(cd hello; echo "Hello Shell" > hello.txt); pwd; cat hello/hello.txt
```

上面我进入了子目录 hello，并创建了一个 hello.txt 文件。输出结果是：

```
Hello Shell
```

可以看到我当前目录没有改变，但是文件已经创建成功了。

#### {} 大括号

用法与上面介绍的指令群组非常相似，但有个不同点，它在当前的 shell 执行，不会产生 subshell。 单纯只使用大括号时，作用就像是个没有指定名称的函数。

```shell
a=2
{ a=1; }
echo $a
```

上面输出：`1`

这个用法和 `()` 用法的区别有两个：

* 大括号 `{}` 里的运算是在当前 Shell 运行，会影响外层结果，而括号 `()`的不会。
* 大括号里最后一个语句必须要用 `;` 分号结束，否则出错，而括号 `()` 的并没有这个要求。

## 逻辑运算符

逻辑运算符有三个，分别是：非运算、或运算、与运算。

* `!`：非运算符。
* `-o`：或运算符。
* `-a`：与运算符。

因为 Shell 中并没有布尔类型，所以非运算符主要是对表达式取反。

```shell
#!/bin/bash
a=10
b=20
# 非运算
if !(( a == b ))
then
   echo "a is not equal to b" 
fi
# 或运算
if [ $a -lt 100 -o $b -gt 100 ]
then
   echo "a < 100 or b > 100" 
fi
# 与运算
if [ $a -lt 100 -a $b -gt 15 ]
then
   echo "a < 100 and b > 15" 
fi
```

值得注意的是，因为 Shell 语言并没有布尔型。所以如果你尝试在非运算符后面跟上一个「布尔值」，那么你会得到错误的结果。

```shell
#!/bin/bash
result=true
if [ !$result ]
then 
  echo "Hello"
fi
```

按照我们的理解，上面的例子应该不会打印出 Hello 字符，但实际结果是会打印。这是因为 Shell 中根本就没有布尔类型的值，所以 if 表达式中的字符串会被当成是一个字符串，字符串肯定就是 true 了，所以就会打印 Hello。其实如果我们随便输入一串字符，结果还是会输出 Hello。

## 关系运算符

关系运算符只支持数值运算，不支持字符运算。

* `-eq`：检测两个数是否相等，相等返回 true。
* `-ne`：检测两个数是否不相等，相等返回 true。
* `-gt`：检测左边的数是否大于右边的，如果是返回 true。
* `-lt`：检测左边的数是否小于右边的，如果是返回 true。
* `-ge`：检测左边的数是否大于等于右边的，如果是返回 true。
* `-le`：检测左边的数是否小于等于右边的，如果是返回 true。