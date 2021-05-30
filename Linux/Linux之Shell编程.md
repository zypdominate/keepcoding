[toc]

### 数组

- 定义数组

  `IPTS=(10.0.0.1 10.0.0.2 10.0.0.3)`

- 显示数组的所有元素

  `echo ${IPTS[@]}`

- 显示数组元素个数

  `echo ${#IPTS[@]}`

- 显示数组的第一个元素

  `echo ${IPTS[0]}`

```shell
root@ubuntu:/home# ipts=(10.0.0.1 10.0.0.2 10.0.0.3)
root@ubuntu:/home# echo $ipts
10.0.0.1
root@ubuntu:/home# echo ${ipts[@]}
10.0.0.1 10.0.0.2 10.0.0.3
root@ubuntu:/home# echo ${#ipts[@]}
3
root@ubuntu:/home# echo ${ipts[0]}
10.0.0.1
root@ubuntu:/home# echo ${ipts[1]}
10.0.0.2
root@ubuntu:/home# echo ${ipts[2]}
10.0.0.3
root@ubuntu:/home# echo ${ipts[3]}

```

---

### 转义与引用

#### 特殊字符

特殊字符：一个字符不仅有字面意义，还有元意（meta-meaning）

- `#` 注释
- `;` 分号
- `\` 转义符号
- `"` `'` 引号

#### 转义符号

单个字符前的转义符号

- `\n \r \t` 单个字符的转义
- `\$ \" \\` 单个非字母的转义

```shell
root@ubuntu:/home# echo "$a"

root@ubuntu:/home# echo "\$a"
$a
```

#### 引号

- `"` 双引号
- `'` 单引号
- `  反引号

```
root@ubuntu:/home# var1=123
root@ubuntu:/home# echo '$var1'
$var1
root@ubuntu:/home# echo "$var1"
123
```

---

### 运算符

#### 赋值运算符

- `=` 赋值运算符，用于算术赋值和字符串赋值



#### 算术运算符

- 基本运算符：`+ - * / ** %    `
- 使用 `expr` 进行运算：`expr 1 + 2`，仅支持整数，+号两侧需要空格

```shell
root@ubuntu:/# expr 1 + 2
3
root@ubuntu:/# num1=`expr 1 + 2`
root@ubuntu:/# echo $num1
3
```



#### 数字常量

- 数字常量的使用方法
  - let “变量名=变量值”
  - 变量值使用0开头为八进制
  - 变量值使用0x开头为十六进制



####  双圆括号

- 双圆括号是 let 命令的简化
  - (( a=10 ))
  - (( a++ ))
  - echo $(( 10+20 ))

```shell
root@ubuntu:/# (( a=1+2 ))
root@ubuntu:/# echo $a
3
root@ubuntu:/# b=2+3
root@ubuntu:/# echo $b
2+3
root@ubuntu:/# (( a++ ))
root@ubuntu:/# echo $a
4
```

---

### 特殊字符大全

#### 引号

- ' 完全引用
- " 不完全引用
- ` 执行命令



#### 括号

- () (()) $()  圆括号

  - 单独使用圆括号会产生一个子 shell  ( xyz=123 )

    ```bash
    [root@bogon ~]# echo $(( 1+2 ))
    3
    ```

    ```bash
    [root@bogon ~]# cmd1=$(ls)
    [root@bogon ~]# echo $cmd1
    Desktop Documents Downloads Music Pictures Public Templates Videos
    ```

  - 数组初始化 IPS=( ip1 ip2 ip3)

- [] [[]] 方括号

  - 单独使用方括号是测试(test)或数组功能

    ```bash
    [root@bogon ~]# [ 5 -gt 4 ]
    [root@bogon ~]# echo $?
    0
    [root@bogon ~]# [ 5 -gt 6 ]
    [root@bogon ~]# echo $?
    1
    ```

  - 两个方括号表示测试表达式

    ```bash
    [root@bogon ~]# [ 5 > 4 ]
    [root@bogon ~]# echo $?
    0
    [root@bogon ~]# [ 5 > 6 ]
    [root@bogon ~]# echo $?
    1
    ```

- <>  尖括号 重定向符合

- {}  花括号

  - 输出范围 echo {0..9}

    ```bash
    [root@bogon ~]# echo {0..9}
    0 1 2 3 4 5 6 7 8 9
    ```

  - 文件复制 cp /etc/passwd{,.bak}

    ```bash
    [root@bogon ~]# cp -v /etc/passwd{,.bak}
    "/etc/passwd" -> "/etc/passwd.bak"
    
    [root@bogon ~]# cp -v initial-setup-ks.cfg{,.txt}
    ‘initial-setup-ks.cfg’ -> ‘initial-setup-ks.cfg.txt’
    ```



#### 运算符合和逻辑符合

- `+ - * / %` 算数运算符
- `> < =` 比较运算符
- `&& || !` 逻辑运算符



#### 转义符号

`\` 转义某字符

- `\n` 普通字符转义后有不同的功能
- `\'` 特殊字符转义后，当做普通字符来使用



#### 其他符号

- `#` 注释符
- `;` 命令分隔符
  - case 语句的分隔符要转义 ;;
- `:`空指令
- `.` 和 source 命令相同
- `~` 家目录
- `,` 分隔目录
- `*` 通配符
- `?` 条件测试 或 通配符
- `$`  取值符
- `|` 管道符
- `&` 后台运行
- ` ` 空格

---

### 测试与判断

- 退出程序命令

  - exit
  - eixt 10 返回10给shell，返回值非0为不正常退出
  - `$?` 判断当前shell前一个进程是否正常退出

- test 命令用于检查文件或者比较值

  - 文件测试
  - 整数比较测试
  - 字符串测试

  测试语句可以简化为 `[ ]` 符号，`[ ]` 符号嗨哟拓展写法 `[[ ]]`，支持 &&  ||  <  > 

  `man  test` 查看具体用法

  ```bash
  [root@bogon ~]# [ $UID=0 ]
  [root@bogon ~]# echo $?
  0
  [root@bogon ~]# echo $USER
  root
  ```

---

### if 判断

```bash
[root@bogon ~]# if [ $UID=0 ]
> then 
>     echo " root user"
> fi
 root user
```

```bash
[root@bogon ~]# if pwd
> then 
>     echo " pwd running "
> fi
/root
 pwd running 
```

`if-then-else`语句可以在条件不成立时也运行相应的命令

```
if [ 测试条件成立]
then 执行命令
else 测试条件不成立，执行相应命令
fi 结束
```

```bash
[root@bogon ~]# cat test.sh 
#!/bin/bash

if [ $USER=root ]; then
    echo "user root"
else 
    echo "oher user"
fi
[root@bogon ~]# . test.sh 
user root
```

```bash
[root@bogon ~]# cat test2.sh 
#!/bin/bash
if [ $USER = root ]; then
    echo "root"
elif [ $USER = user1 ]; then
    echo "user1"
else
    echo "other user"
fi
[root@bogon ~]# bash ./test2.sh 
root
```

---

### case

case 语句和 select 语句可以构成分支

```shell
case "$var" in
    "case1")
    cmd1  ;;
    "case2")
    cmd2  ;;
    *)
    cmd3  ;;
esac
```

```shell
foxit@ubuntu:~$ cat test.sh 
#!/bin/bash
case "$1" in
    "start"|"START")
    echo $0 start......
    ;;

    "stop")
    echo $0 stop......
    ;;

    "restart" | "reload")
    echo $0 restart......
    ;;
    *)
    echo "Usage: $0 {start|stop|restart|reload}"
    ;;
esac
foxit@ubuntu:~$ ./test.sh start
foxit@ubuntu:~$ ./test.sh start
./test.sh start......
foxit@ubuntu:~$ ./test.sh stop
./test.sh stop......
```

---

### for 循环

- 使用 for 循环变量命令的执行结果
- 使用 for 循环变量变量和文件的内容
- C语言风格的 for 命令
- while  循环
- 死循环
- until 循环
- break 和 continue 语句
- 使用循环对命令行参数的处理

```shell
foxit@ubuntu:~$ echo {1..9}
1 2 3 4 5 6 7 8 9
foxit@ubuntu:~$ for i in {1..3}
> do
>   echo $i
> done
1
2
3
```

```shell
foxit@ubuntu:~$ touch a.mp3 b.mp3 c.mp3
foxit@ubuntu:~$ ls
a.mp3  b.mp3  c.mp3
foxit@ubuntu:~$ for filename in `ls *.mp3`
> do
>    mv $filename $(basename $filename .mp3).mp4
> done
foxit@ubuntu:~$ ls
a.mp4  b.mp4  c.mp4

foxit@ubuntu:~$ for filename in $(ls *.mp4); do    mv $filename $(basename $filename .mp4).mp3; done
foxit@ubuntu:~$ ls
a.mp3  b.mp3  c.mp3 
```

```shell
foxit@ubuntu:~$ for ((i=1;i<=3;i++))
> do 
>   echo $i
> done
1
2
3
```

```shell
foxit@ubuntu:~$ a=1
foxit@ubuntu:~$ while [ $a -lt 10 ]
> do
>   echo $a
> done

foxit@ubuntu:~$ while [ $a -lt 4 ]; do  ((a++));echo $a; done
2
3
4
```

```shell
foxit@ubuntu:~$ for num in {1..9}
> do
>   if [ $num -eq 5 ]; then
>     break
>   fi
>   echo $num
> done
1
2
3
4
```

```shell
foxit@ubuntu:~$ for num in {1..9}
> do
>   if [ $num -lt 5 ]; then
>      continue
>   fi
>   echo $num
> done
5
6
7
8
9
```

---

### 使用循环处理命令行参数

- 命令行参数可以使用 `$1 $2 ... ${10}...${n}` 进行读取
- $0 表示脚本名称
- $* 和 $@ 代表所有位置参数
- $# 代表位置参数的数量

```shell
foxit@ubuntu:~$ cat test.sh 
#!/bin/bash
for pos in $*
do
    if [ $pos = help ]; then
        echo $pos $pos
    fi
done

foxit@ubuntu:~$ ./test.sh help
help help
```

```shell
foxit@ubuntu:~$ cat test.sh 
#!/bin/bash
while [ $# -ge 1 ]
do
  if [ "$1" = "help" ]; then
    echo $1 $1
  fi
  shift
done

foxit@ubuntu:~$ ./test.sh a b c help
help help
```

---

### 自定义函数

- 函数用于“包含”重复使用的命令集合

- 自定义函数

  function fname() {

  命令

  }

- 函数的执行

  fname

```shell
foxit@ubuntu:~$ function cdls() {
> cd /var
> ls
> }
foxit@ubuntu:~$ cdls
backups  cache  crash  lib  local  lock  log  mail  metrics  opt  run  snap  spool  tmp
foxit@ubuntu:~$ unset cdls
```

- 函数作用范围的变量

  local 变量名

- 函数的参数

  $1 $2 $3 ... $n

```shell
foxit@ubuntu:~$ cdls() { 
dir=$1
cd $dir
ls
}

foxit@ubuntu:/tmp$ cdls /var
backups  cache  crash  lib  local  lock  log  mail  metrics  opt  run  snap  spool  tmp
```

```shell
foxit@ubuntu:~$ cat test.sh 
#!/bin/bash
checkpid() {
local i
for i in $*; do
    [ -d "/proc/$i" ] && return 0
done
return 1
}
foxit@ubuntu:~$ chmod u+x test.sh
foxit@ubuntu:~$ source test.sh 
foxit@ubuntu:~$ checkpid 1
foxit@ubuntu:~$ echo $?
0
foxit@ubuntu:~$ checkpid 2  3
foxit@ubuntu:~$ echo $?
0
foxit@ubuntu:~$ checkpid 65533
foxit@ubuntu:~$ echo $?
1
```

---

### 计划任务

#### 一次性计划任务

`at` 执行定时任务
`ctrl+d` 提交
`atq` 查看定时任务

```shell
foxit@ubuntu:~$ at 13:45
The program 'at' is currently not installed. You can install it by typing:
sudo apt install at
foxit@ubuntu:~$ sudo apt install at

foxit@ubuntu:~$ at 13:47
warning: commands will be executed using /bin/sh
at> echo hellotxt > /home/foxit/hello.txt
at> <EOT>
job 2 at Sun May 30 13:47:00 2021
foxit@ubuntu:~$ ls
Desktop  Documents  Downloads  examples.desktop  hello.txt  Music  Pictures  Public  Templates  Videos
foxit@ubuntu:~$ cat hello.txt 
hellotxt
foxit@ubuntu:~$ ls -l hello.txt 
-rw-rw-r-- 1 foxit foxit 9 5月  30 13:47 hello.txt
```



#### 周期性计划任务

**cron**

- 配置方式
  - `crontab -e`
- 查看现有的计划任务
  - `crontab -l`
- 配置格式
  - 分钟  小时  日期  月份  星期  执行的命令
  - 注意命令的路径问题

```shell
foxit@ubuntu:~$ crontab -e
* * * * * /bin/date/date >> /home/foxit/tmp.txt

foxit@ubuntu:~$ cat tmp.txt 
2021年 05月 30日 星期日 13:56:01 CST
2021年 05月 30日 星期日 13:57:01 CST
```

---

#### 为脚本加锁

- 如果计算机不能按照预期时间运行
  - `anacontab` 延时计划任务
  - `flock` 锁文件



























