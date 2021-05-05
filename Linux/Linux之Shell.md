[toc]

### 脚本不同执行方式的影响

标准shell脚本包含哪些元素

- "#" 号开头的注释
- chmod u+rx filename 可执行权限
- 执行命令
  - `bash ./filename.sh`
  - `./filename.sh`   需要有可执行权限
  - `source ./filename.sh`
  - `. filename.sh`
- 备注：前两种执行方式，对当前运行环境没有影响（会产生一个子进程，sh脚本中在子进程中执行，执行结束回到父进程）；后两种则造成影响；

内建命令与外部命令：

- 内建命令不需要创建子进程（比如 cd，pwd）；
  外部命令才会创建子进程，所以内建命令能改变当前shell的环境
- 内建命令对当前 Shell 生效；
  如果使用bash生成了一个新的子进程，那么内置命令会对新产生这个子进程生效，一旦你在子进程使用了exit回到了父进程之后，子进程里执行的内部命令就无效了

---

### 管道

- 管道和信号一样，也是进程通信的方式之一
- 匿名管道（管道符）是 Shell 编程常用到的通信工具
- 管道符是 `|`，将一个命令执行结果传递给后面的命令
  - `ps |cat`
  - `echo 123 |ps`
  - `cat filename |more`

 demo

```cmd
root@ubuntu:/home# cat |ps -f
UID        PID  PPID  C STIME TTY          TIME CMD
root      1033   942  0 11:03 pts/8    00:00:00 -bash
root      1588  1033  0 17:15 pts/8    00:00:00 cat
root      1589  1033  0 17:15 pts/8    00:00:00 ps -f
```

```cmd
root@ubuntu:/home# cd /
root@ubuntu:/# cd /proc/1588
root@ubuntu:/proc/1588# ls
attr       cgroup      comm             cwd      fd       io        map_files  mountinfo   net        oom_adj        pagemap      projid_map  schedstat  smaps         stat    syscall  timerslack_ns
autogroup  clear_refs  coredump_filter  environ  fdinfo   limits    maps       mounts      ns         oom_score      patch_state  root        sessionid  smaps_rollup  statm   task     uid_map
auxv       cmdline     cpuset           exe      gid_map  loginuid  mem        mountstats  numa_maps  oom_score_adj  personality  sched       setgroups  stack         status  timers   wchan
root@ubuntu:/proc/1588# cd fd
root@ubuntu:/proc/1588/fd# ls -l
total 0
lrwx------ 1 root root 64 5月   3 17:19 0 -> /dev/pts/8
l-wx------ 1 root root 64 5月   3 17:19 1 -> pipe:[4227611]
lrwx------ 1 root root 64 5月   3 17:15 2 -> /dev/pts/8
```

这里的 0 表示标准输入（终端），1  表示标准输出（管道），2 表示标准错误输出；使用管道符时尽量规避内建命令。

---

### 重定向

- 一个进程默认会打开标准输入、标准输出、错误输出三个文件描述符

- 输入重定向符合  `<`： 

  ```cmd
  root@ubuntu:/# wc -l 
  123
  123
  1
  3
  root@ubuntu:/# wc -l < /etc/passwd
  42
  ```

  ```cmd
  root@ubuntu:/home# read var
  100
  root@ubuntu:/home# echo $var
  100
  
  root@ubuntu:/home# read var2 < test.txt 
  root@ubuntu:/home# echo $var2
  123
  ```

- 输出重定向符合 `>`、`>>`、`2>`、`&>`

  `>` 重定向，`>>`重定向追加，`2>`错误输出重定向，`&>`所有输出重定向

  ```cmd
  root@ubuntu:/home# echo $var2 > b.txt
  root@ubuntu:/home# cat b.txt 
  123
  root@ubuntu:/home# echo $var2 >> b.txt
  root@ubuntu:/home# cat b.txt 
  123
  123
  root@ubuntu:/home# nocmd 2> error.txt
  root@ubuntu:/home# ls
  b.txt  error.txt
  root@ubuntu:/home# cat error.txt 
  No command 'nocmd' found, did you mean:
   Command 'nxcmd' from package 'libnxcl-bin' (universe)
  nocmd: command not found
  
  root@ubuntu:/home# ls && nocmd &> all.txt
  b.txt  error.txt
  root@ubuntu:/home# cat all.txt 
  No command 'nocmd' found, did you mean:
   Command 'nxcmd' from package 'libnxcl-bin' (universe)
  nocmd: command not found
  ```

- 输入和输出重定向组合使用

  ```cmd
  root@ubuntu:/home# vi a.sh 
  #!/bin/bash
  # cat << EOF > /home/b.sh
  cat > /home/b.sh << EOF
  echo "hello bash"
  EOF
  
  root@ubuntu:/home# bash ./a.sh 
  root@ubuntu:/home# cat b.sh 
  echo "hello bash"
  ```

---

### 变量

#### 变量赋值

- 变量名=变量值

  ```shell
  a=123
  ```

- 使用`let`为变量赋值

  ```cmd
  let a=10+20
  ```

- 将命令赋值给变量

  ```shell
  l=ls
  ```

- 将命令结果赋值给变量，使用 `$()` 或者 ``

  ```shell
  letc=$(ls -l /etc)
  ```

- 变量值有空格等特殊字符可以包含在 “ ” 或 ‘’ 中

---

#### 变量的引用

- `${变量名}`称作对变量的引用
- `echo ${变量名}`查看变量的值
- `${变量名}`在部分情况下可以省略为 `$变量名`

```shell
[foxit@localhost ~]$ str1="hello"
[foxit@localhost ~]$ echo ${str1}
hello
[foxit@localhost ~]$ echo $str1
hello
[foxit@localhost ~]$ echo ${str1}23
hello23
[foxit@localhost ~]$ echo $str123

```

---

#### 变量的作用范围

- 变量的导出：`export`
- 变量的删除：`unset`

```shell
[foxit@localhost ~]$ a=1
[foxit@localhost ~]$ echo $a
1
[foxit@localhost ~]$ bash
[foxit@localhost ~]$ echo $a

[foxit@localhost ~]$ exit
exit
[foxit@localhost ~]$ echo $a
1
```

```shell
root@ubuntu:/# demo_var="hello subshell"
root@ubuntu:/# vim test_demo.sh
echo ${demo_var}
root@ubuntu:/# chmod u+x test_demo.sh 
root@ubuntu:/# bash test_demo.sh 

root@ubuntu:/# ./test_demo.sh 

root@ubuntu:/# source test_demo.sh 
hello subshell
root@ubuntu:/# . test_demo.sh 
hello subshell
```

`bash` 进入子 Shell，`exit` 退出

```shell
root@ubuntu:/# export demo_var
root@ubuntu:/# 
root@ubuntu:/# bash test_demo.sh 
hello subshell
root@ubuntu:/# ./test_demo.sh 
hello subshell
```

```shell
root@ubuntu:/home# unset demo_var
root@ubuntu:/home# echo ${demo_var}

```

---

### 系统环境变量

环境变量：每个 Shell 打开都可以获取到的变量

- `set`  和 `env` 命令

- `$?$$$0`

  `$?` 上一条命令是否执行成功
  `$$` 显示当前进程pid
  `$0` 当前进程名称

- `$PATH`

- `$PS1`

位置变量

- `$1$2...$n`

查看环境变量：`env |more`，`set |more`



```shell
root@ubuntu:/home# echo $USER
root
root@ubuntu:/home# echo $UID
0
root@ubuntu:/home# echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

root@ubuntu:/home# PATH=$PATH:/home
root@ubuntu:/home# echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home
```

```shell
root@ubuntu:/home# cat test_demo.sh 
echo $$
echo $0
root@ubuntu:/home# . test_demo.sh 
1695
-bash
root@ubuntu:/home# ./test_demo.sh 
7516
./test_demo.sh
```

```shell
root@ubuntu:/home# cat test_demo.sh 
#!/bin/bash
echo $1
echo ${2-_}

root@ubuntu:/home# ./test_demo.sh 11 
11
_
root@ubuntu:/home# ./test_demo.sh 11 22
11
22
```



