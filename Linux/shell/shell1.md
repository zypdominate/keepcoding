## 如何运行shell脚本

- 通过bash命令
- 作为可执行程序

例如: 一个shell脚本,保存为hello.sh

```shell
#!/bash/bash
echo "hello world"
```

若想用可执行程序运行,需要先修改文件的权限,再执行脚本

```shell
chmod +x ./hello.sh  # 使脚本具有执行权限
./hello.sh 	 	# 执行脚本
```

## 如何标记语句的结束

在shell中标记语句的结束有两种方式: 分号,换行

```shell
a=10
if [ $a = 10 ]; then
	echo "the value of a is 10"
fi 
```

或者写成:

```shell
a=10
if [ $a =10 ]
then 
	echo "the value of a is 10"
fi
```

## 基本数据类型

shell 语言是一门弱类型的语言,没有数据类型上的概念. 无论输入的是字符串还是数字,在shell中都是按照字符串类型来存储. 至于具体是什么类型, shell根据上下文去确定.

```shell
#!/bin/bash
num="Hello"
echo `expr $num + 1`	//expr: not a decimal number: 'Hello'
num=1
echo `expr $num + 1`	//2
```

这是因为虽然 Shell 语言是弱语言类型，但其解释执行的时候会进行语法检查。**意识到 Shell 在数据类型上的特殊性很重要，这样你就不会犯一些基础错误了。**例如下面的例子：

```shell
result="false"
if $result
then
	echo "true."
else 
	echo "false."	# 输出false
fi
```

虽然上面的 result 变量是一个字符串，但是实际上在运行时，Shell 是将其当成一个布尔型的值进行比较的。当你将 result 改成 true 之后，结果便会输出 true。

## 变量的使用

shell语言是一门若语言类型, 所以变量可以无须定义便可直接使用.

- 直接使用$符号引用

```shell
str="hello shell"
echo $str
```

- 使用${} 符号引用

```shell
str="hello shell"
echo ${str}
```

一般来说，如果不会引起变量的阅读困难，那么可以使用第一种变量引用方式。但如果在较为复杂的环境，会引起阅读和理解困难，那还是使用第二种引用方式。例如：

```shell
#!/bin/sh
echo "what is your name?"
read USERNAME
echo "hello $USERNAME"
echo "create an email $USERNAME@163.com for you"
echo "create an email ${USERNAME}@163.com for you"
```

最好统一的规范的加上大括号.

## 打印字符串

### echo

在一般使用echo命令打印字符串. echo后的形式: 裸奔,单引号,双引号

1. 裸奔: shell后面什么都不加,直接写上要输出的字符串

```shell
echo i must prctice shell language
```

这种方式会直接输出 echo 命令后的所有字符，例如上面会输出：` i must prctice shell language`。但这种方式有个缺陷，就是无法输出分号`;`。因为当读到分号的时候，程序会认为这一行代码结束了。

```shell
echo I must practice ; learn shell language .
# I must practice 
# -bash: learn: command not found
# 程序只输出了 ;以前的内容，并把后面的learn当成了一个命令。
```

2. 单引号的引用方式

```shell
str='hello shell language'
echo $str
```

但这种方式的缺陷是无法在字符串中引用变量。

```shell
NAME="shell"
str='Hello ! My Name is $NAME';
echo $str
# Hello ! My Name is $NAME
```

3. 双引号的引用方式

```shell
NAME="shell"
str="Hello! My Name is $NAME";
echo $str
# Hello! My Name is shell
```

在双引号的引用方式下，我们可以成功打印出 NAME 变量的值。但是这种方式也有其缺陷，就是无法直接打印出特殊字符，需要把特殊进行转义。

### printf

使用 printf 命令可以对齐打印字符串，对于阅读比较友好。

```shell
#!/bin/bash
printf "%-10s %-8s %-4s\n" 姓名 年龄 存款K  
printf "%-10s %-8s %-4.2f\n" 郭靖 30 52.20
printf "%-10s %-8s %-4.2f\n" 杨过 25 26.32
printf "%-10s %-8s %-4.2f\n" 郭芙 27 15.20
```

`%-10s`，百分号是个标识符，`-`表示左对齐，数字10表示保留10位的长度，s表示其实一个字符串。

例如: 对应的%-8s表示左对齐,保留8位,是字符串 ; 对应的%-4.2f表示左对齐,保留4位,小数点保留两位,是个浮点型数字.

## 如何进行数学运算

 Shell 的数学运算和我们高级语言中的语法完全不一样。Shell 中把所有东西都当成是一个字符串，所以这里它并不知道我们要它进行数学运算。实际上在 Shell 中你要进行这样的数学运算，你应该这么写：

```shell
#!/bin/bash
a=`expr 10 + 5`
echo $a
```

```shell
#!/bin/bash
let a=10+5
echo $a
```

```shell
(( a = 10 + 5 ))
echo $a
```

## 如何进行数值比较

```shell
#!/bin/bash
a=15
b=10
if (( a >= b))
then 
	echo "a >= b"
else
	echo "a < b"
fi
```

```shell
#!/bin/bash
a=15
if (( a > 10 && a < 20 ))
then 
	echo "10 < a < 20"	
else
	echo "a <= 10 or a >= 20"
fi
```

## 如何进行字符串比较

在shell中进行字符串比较有换门的留六个操作符

* `=`：检测两个字符串是否相等，相等返回 true。
* `!=`：检两个字符串是否相等，不相等返回 true。
* `-z`：检测字符串长度是否为0，为 0 返回 true。
* `-n`：检测字符串长度是否为0，不为 0 返回 true。
* `str`：检测字符串是否为空，不为空返回 true。

**要记得操作符左右两边都要加空格，否则会报语法错误。**

```shell
#!/bin/bash
a="abc"
b="efg"
# 字符串是否相等
if [ $a = $b ]
then
   echo "$a = $b : a 等于 b"
else
   echo "$a = $b: a 不等于 b"
fi
if [ $a != $b ]
then
   echo "$a != $b : a 不等于 b"
else
   echo "$a != $b: a 等于 b"
fi
# 字符串长度是否为0
if [ -z $a ]
then
   echo "-z $a : 字符串长度为 0"
else
   echo "-z $a : 字符串长度不为 0"
fi
if [ -n "$a" ]
then
   echo "-n $a : 字符串长度不为 0"
else
   echo "-n $a : 字符串长度为 0"
fi
# 字符串是否为空
if [ $a ]
then
   echo "$a : 字符串不为空"
else
   echo "$a : 字符串为空"
fi

# abc = efg: a 不等于 b
# abc != efg : a 不等于 b
# -z abc : 字符串长度不为 0
# -n abc : 字符串长度不为 0
# abc : 字符串不为空
```

## 循环结构

####for 循环结构

```shell
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done
```

```shell
for loop in 1 2 3 4 5
do
  echo "The value is: $loop"
done
# The value is: 1
# The value is: 2
# The value is: 3
# The value is: 4
# The value is: 5
```

```shell
for str in 'This is a string'
do
  echo $str
done
# This is a string
```

#### while 循环

```shell
while condition
do
    command
done
```

```shell
#!/bin/sh
a=1
while [ $a -lt 5 ]
do
    echo $a
    let "a++"
done
# 1
# 2
# 3
# 4
```

#### case 语句

```shell
case 值 in
模式1)
    command1
    command2
    ...
    commandN
    ;;
模式2）
    command1
    command2
    ...
    commandN
    ;;
*)
	  command1
    ....
    commandN
	  ;;
esac
```

case 语句取值后面必须为单词 in，每一模式必须以右括号结束。取值可以为变量或常数。匹配发现取值符合某一模式后，其间所有命令开始执行直至 ;;。取值将检测匹配的每一个模式。一旦模式匹配，则执行完匹配模式相应命令后不再继续其他模式。如果无一匹配模式，使用星号 * 捕获该值，再执行后面的命令。case 语句使用 esac 作为结束标志。

```shell
#!/bin/bash
echo '输入 1 到 4 之间的数字:'
echo '你输入的数字为:'
read aNum
case $aNum in
    1)  echo '你选择了 1'
    ;;
    2)  echo '你选择了 2'
    ;;
    3)  echo '你选择了 3'
    ;;
    4)  echo '你选择了 4'
    ;;
    *)  echo '你没有输入 1 到 4 之间的数字'
    ;;
esac
```

#### 跳出循环

break 和 continue

```shell
#!/bin/bash
while true
do
    echo -n "输入 1 到 5 之间的数字:"
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的! 游戏结束"
            break
        ;;
    esac
done
# 输入 1 到 5 之间的数字:3
# 你输入的数字为 3!
# 输入 1 到 5 之间的数字:7
# 你输入的数字不是 1 到 5 之间的! 游戏结束

# continue
# continue命令与break命令类似，只有一点差别，它不会跳出所有循环，仅仅跳出当前循环。
```

```shell
#!/bin/bash
while :
do
    echo -n "输入 1 到 5 之间的数字: "
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的!"
            continue
            echo "游戏结束"
        ;;
    esac
done
# 当输入大于5的数字时，该例中的循环不会结束，语句 echo 「游戏结束」永远不会被执行。
```
