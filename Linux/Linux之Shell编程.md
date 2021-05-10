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





