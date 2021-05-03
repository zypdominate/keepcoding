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











