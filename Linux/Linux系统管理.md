[toc]

### 软件包管理器

- CentOS、RedHat：yum，软件安装包格式为rpm
- Debian、Ubuntu：apt，软件包格式为deb

#### rpm 包

- 格式

  `vim-common-7.4.10-5.el7.x86_64.rpm`
  vim-common：软件名
  7.4.10-5：软件版本
  el7：系统版本
  x86_64：平台

- 命令

  `-q` 查询软件包
  `-i` 安装软件包
  `-e` 卸载软件包

  示例：

  ```shell
  mount /dev/sr0  /mnt   # 将/dev/sro 挂载到/mnt
  rpm -qa |more   # 查看所有安装的rpm包
  rpm -q zlib			# 查看特定包
  zlib-1.2.7-18.el7.x86_64
  rpm -e zlib			# 卸载特定包
  ```


---

#### yum 包管理器

- CenOS yum 源

  http://mirror.centos.org/centos/7/

- 国内镜像

  http://opsx.alibaba.com/mirror

---

### 进程管理

#### 进程的概念与进程查看

- 进程是运行中的程序，从程序开始运行时到终止的整个生命周期是可管理的
  - C程序的启动是从 main 函数开始的
    - int main(int agrc, char *argv[])
    - 终止的方式并不唯一
      - 正常终止：从 main 返回、调用 exit 等方式
      - 异常终止：调用 abort、接收信号

- 进程的查看

  - `ps`

    - `ps -efL | more`, L 展示线程相关信息
    - `ps -aux |grep xxx`

  - `pstree`

  - `top`

    ```cmd
    [root@bogon /]# top
    top - 15:01:17 up 46 days, 23:58,  3 users,  load average: 0.01, 0.02, 0.10
    Tasks: 365 total,   3 running, 362 sleeping,   0 stopped,   0 zombie
    %Cpu(s):  8.0 us,  4.2 sy,  0.0 ni, 87.7 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
    KiB Mem : 16266732 total,  8432380 free,  2492776 used,  5341576 buff/cache
    KiB Swap:  8257532 total,  7626024 free,   631508 used. 12474864 avail Mem 
    
      PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND                       
     6229 polkitd   20   0  620296  10428   2416 S  14.6  0.1   9623:41 polkitd
     6201 dbus      20   0   90400  16244    840 S   9.0  0.1   5933:48 dbus-daemon     
    ```

    up 46 days 开机后运行时间；3 users 当前登录用户数；

    load average 系统平均负载(衡量系统繁忙程度)，后面分别是1分钟、5分钟、15分钟表示的繁忙程度，值为1时表示满负载，若从右至左值变大表示系统越来越繁忙；

    %Cpu(s) 表示系统各个部分占用的比例：us 用户，sy 系统，id 空闲状态，wa 等待磁盘IO操作；括号中的s表示多个cpu，按数字1可罗列所有cpu状态；

    KiB Mem 内存，total 总共，free 没有在使用，used 在使用，buff/cache 读写缓存；

    KiB Swap 交换分区（相当于windows中虚拟内存）；

---

#### 进程的控制命令

- 调整优先级

  - nice 范围从 -20 到19， 值越小优先级越高，抢占资源越来越多
  - renice 重新设置优先级

- 进程的作业控制

  - jobs
  - & 符号

- demo 脚本

  ```shell
  [root@bogon Videos]# cat process_test.sh 
  #!/bin/bash
  echo $$
  while :
  do
    :
  done
  ```

- 进程的作业控制demo

  - 后台运行：`&`

    ```shell
    [root@bogon Videos]# ./process_test.sh &
    [1] 21271
    [root@bogon Videos]# 21271
    ```

  - 将后台运行的程序调回前台：`jobs`

    ```shell
    [root@bogon Videos]# jobs
    [1]+  Running                 ./process_test.sh &
    [root@bogon Videos]# fg 1
    ./process_test.sh
    
    ```

  - 至为后台挂起：`Ctrl + z`

    ```shell
    [root@bogon Videos]# fg 1
    ./process_test.sh
    ^Z
    [1]+  Stopped                 ./process_test.sh
    [root@bogon Videos]# 
    
    ```

    查看进程，S的状态变为T，stopped，此时作业处于暂停状态：

    ```shell
    [root@bogon Videos]# top -p 21271
    top - 16:07:52 up 47 days,  1:05,  4 users,  load average: 0.23, 0.74, 1.05
    Tasks:   1 total,   0 running,   0 sleeping,   1 stopped,   0 zombie
    %Cpu(s):  7.8 us,  4.3 sy,  0.0 ni, 87.7 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
    KiB Mem : 16266732 total,  8418980 free,  2503760 used,  5343992 buff/cache
    KiB Swap:  8257532 total,  7627560 free,   629972 used. 12463808 avail Mem 
    
      PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND         
    21271 root      20   0  113284   1184   1000 T   0.0  0.0   7:53.22 process_test.sh 
    ```

    暂停后，又想让该程序起来：

    ```shell
    [root@bogon Videos]# jobs
    [1]+  Stopped                 ./process_test.sh
    
    ```

    接着，可以使用 `fg 1`前台继续运行，或者 `bg 1`置为后台运行。

- 优先级 demo

  ```shell
  [root@bogon Videos]# chmod u+x process_test.sh 
  [root@bogon Videos]# ls -l process_test.sh 
  -rwxr--r--. 1 root root 43 Nov 15 15:34 process_test.sh
  [root@bogon Videos]# 
  [root@bogon Videos]# id
  uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
  [root@bogon Videos]# ./process_test.sh 
  30017
  
  ```

  在另一个窗口使用 `top -p 进程号` 查看进程：

  ```shell
  [root@bogon Videos]# top -p 30017
  top - 15:43:12 up 47 days, 40 min,  4 users,  load average: 1.94, 1.75, 1.24
  Tasks:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
  %Cpu(s): 32.8 us,  4.3 sy,  0.0 ni, 62.8 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
  KiB Mem : 16266732 total,  8420784 free,  2501324 used,  5344624 buff/cache
  KiB Swap:  8257532 total,  7627560 free,   629972 used. 12466240 avail Mem 
  
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND             
  30017 root      20   0  113284   1184   1000 R 100.0  0.0   6:19.54 process_test.sh  
  ```

  使用 nice 将优先级降低：

  ```shell
  [root@bogon Videos]# nice -n 10 ./process_test.sh 
  20151
  
  ```

  在另一个窗口查看可以看到 NI 值变为 10：

  ```shell
  [root@bogon Videos]# top -p 20151
  top - 15:50:31 up 47 days, 47 min,  4 users,  load average: 1.21, 1.64, 1.42
  Tasks:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
  %Cpu(s):  7.7 us,  4.3 sy, 25.1 ni, 62.8 id,  0.0 wa,  0.0 hi,  0.1 si,  0.0 st
  KiB Mem : 16266732 total,  8419512 free,  2503440 used,  5343780 buff/cache
  KiB Swap:  8257532 total,  7627560 free,   629972 used. 12464124 avail Mem 
  
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND             
  20151 root      30  10  113284   1184   1004 R 100.0  0.0   0:18.55 process_test.sh   
  ```

  不中断当前程序，再创建一个窗口来改变程序优先级，然后去查看 top 中的 NI值相应地改变：

  ```shell
  [root@bogon Videos]# renice -n 15 20151
  20151 (process ID) old priority 10, new priority 15
  ```

---

#### 进程的通信方式—信号

- 信号时进程间通信方式之一，常用：终端用户输入中断命令，通过信号机制停止一个程序的运行。
- 使用信号的常用快捷键和命令
  - `kill -l`
    - SIGINT  通知前台进程终止进程  ctrl + c
    - SIGKILL 立即结束程序，不能被阻塞和处理 `kill -9 pid`

---

#### 守护进程和系统日志

- 使用 nohup 与 & 符号配合运行一个命令
  - nohup 与 & 合用，关闭终端，程序仍然进行
  - nohup 命令使进程忽略 hangup 信号，并把输出追加到 nohup.out 
- 守护进程（daemon）和一般进程的区别：前者可以脱离终端
- 使用 screen 命令
  - `yum install screen` 安装
  - screen 进入 screen 环境
  - ctrl +a+d 退出（detached）screen 环境
  - screen -ls 查看 screen 的会话
  - screen -r sessionid 恢复会话

---

#### 服务管理工具 systemctl

服务（提供常见功能的守护进程）集中管理工具

- service
  - service 服务放在 `/etc/init.d` 目录下
- systemctl
  - systemctl start|stop|restart|reload|enable|disable 服务名称
  - 软件包安装的服务单元 `/usr/lib/systemd/system`

