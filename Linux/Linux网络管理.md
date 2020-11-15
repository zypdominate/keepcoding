[toc]

### 网络管理

#### 网络状态查看

- ifconfig

  eth0 第一块网卡（网络接口）

  这里我的是Ubuntu虚拟机，第一个网络接口是 eth0 

  ```cmd
  root@zyp-virtual-machine:/# ifconfig
  eth0      Link encap:以太网  硬件地址 00:0c:29:cb:3d:56  
            inet 地址:192.168.171.129  广播:192.168.171.255  掩码:255.255.255.0
            inet6 地址: fe80::20c:29ff:fecb:3d56/64 Scope:Link
            UP BROADCAST RUNNING MULTICAST  MTU:1500  跃点数:1
            接收数据包:40109 错误:0 丢弃:0 过载:0 帧数:0
            发送数据包:44089 错误:0 丢弃:0 过载:0 载波:0
            碰撞:0 发送队列长度:1000 
            接收字节:4456689 (4.4 MB)  发送字节:10033944 (10.0 MB)
  
  lo        Link encap:本地环回  
            inet 地址:127.0.0.1  掩码:255.0.0.0
            inet6 地址: ::1/128 Scope:Host
            UP LOOPBACK RUNNING  MTU:65536  跃点数:1
            接收数据包:1446 错误:0 丢弃:0 过载:0 帧数:0
            发送数据包:1446 错误:0 丢弃:0 过载:0 载波:0
            碰撞:0 发送队列长度:1000 
            接收字节:112637 (112.6 KB)  发送字节:112637 (112.6 KB)
  ```

  第一网络接口的其他名称：

  - eno1 板载网卡
  - ens33  PCI-E 网卡
  - enp0s3 无法获取物理信息的PCI-E网卡

- 网络接口命令修改（网卡名称固定之后，方便编写多主机批量控制脚本）

  - 网卡命名规则受 biosdevname 和 net.ifnames 两个参数影响

  - 编辑 /etc/default/grub 文件， 增加 biosdevname=0 net.ifnames=0

    `GRUB_CMDLINE_LINUX="biosdevname=0 net.ifnames=0"`

  - 更新 grub： 执行命令 `update-grub`或者`grub-mkconfig -o /boot/grub/grub.dfg`

  - 编辑 /etc/network/interfaces文件，这边是动态配置：

    ```cmd
    auto eth0
    iface eth0 inet dhcp
    ```

  - 重启 reboot

    |       | biosdevname | net.ifnames | 网卡名 |
    | ----- | ----------- | ----------- | ------ |
    | 默认  | 0           | 1           | ens33  |
    | 组合1 | 1           | 0           | em1    |
    | 组合2 | 0           | 0           | eth0   |

- mii-tool eth0  查看网卡物理连接情况

  ```cmd
  root@zyp-virtual-machine:/# mii-tool eth0
  eth0: negotiated 1000baseT-FD flow-control, link ok
  ```

- route  查看网关

  - route -n 

---

#### 网络配置

- 网卡配置
  - `ifconfig <接口> <IP地址> [netmask 子网掩码]` 设置 IP 地址
    - `ifconfig eth0 192.168.171.126`
    - `ifconfig eth0 192.168.171.126 netmask 255.255.255.0`
  - `ifup <接口>`  网卡启用
    - `ifup eth0`
  - `ifdown <接口>`   网卡关闭
    - `ifdown eth0`
  - `service networking restart` 重启网络配置

- ip 命令
  - `ip addr ls `
    - ifconfig
  - `ip link set dev eth0 up`
    - ifup eth0
  - `ip addr add xxx.0.0.1/24 dev eth1`
    - ifconfig eth1 xxx.0.0.1 netmask 255.255.255.0
  - `ip route add xxx.0.0.1/24 via 192.168.0.1`
    - route add -net xxx.0.0.0 netmask 255.255.255.0 gw 192.168.0.1

---

#### 路由命令

添加、删除网关

- `route -n` 查看网关

- `route add default gw <网关ip> `

- `route add -host <指定ip> gw <网关ip>`

  例如`route add -host 192.168.171.11 gw 192.168.171.1`

- `route add -net <指定网段> netmask <子网掩码> gw <网关ip>`

  例如`route add -net 192.168.0.0 netmask 255.255.255.0 gw 192.168.171.11`

- 删除时将 add 改为 del

---

#### 网络故障管理

- 我当前的 Ubuntu 路由状态：

  ```cmd
  root@zyp-virtual-machine:/# route -n
  内核 IP 路由表
  目标            网关            子网掩码        标志  跃点   引用  使用 接口
  0.0.0.0         192.168.171.2   0.0.0.0         UG    0      0        0 eth0
  169.254.0.0     0.0.0.0         255.255.0.0     U     1000   0        0 eth0
  192.168.171.0   0.0.0.0         255.255.255.0   U     0      0        0 eth0
  ```

- ping  查看当前主机和目标主机是否畅通

- trackroute  追踪路由、服务器的每一跳

  ```cmd
  root@zyp-virtual-machine:/# traceroute -w 1 www.baidu.com
  traceroute to www.baidu.com (182.61.200.7), 30 hops max, 60 byte packets
   1  192.168.171.2 (192.168.171.2)  0.370 ms  0.204 ms  0.577 ms
   2  * * *  (中间的主机如果不支持traceroute，以*的方式展示)
  ```

- mtr  看是否有数据包丢失

- nslookup  查看域名对应的 ip 

  ```cmd
  root@zyp-virtual-machine:/# nslookup www.baidu.com
  Server:		114.114.114.114   这里可以看出是通过哪个DNS服务器来进行的域名解析
  Address:	114.114.114.114#53
  
  Non-authoritative answer:
  www.baidu.com	canonical name = www.a.shifen.com.
  Name:	www.a.shifen.com
  Address: 182.61.200.7
  Name:	www.a.shifen.com
  Address: 182.61.200.6
  
  ```

- telnet

  畅通：

  ```cmd
  root@zyp-virtual-machine:/# telnet www.baid.com 80
  Trying 47.254.33.193...
  Connected to www.baid.com.
  Escape character is '^]'.   
  ```

  端口不可达：

  ```cmd
  root@zyp-virtual-machine:/# telnet www.baid.com 890
  Trying 47.254.33.193...
  telnet: Unable to connect to remote host: Connection refused
  ```

- tcpdump

  - `port xx`  指定端口 

    抓取 任意的网卡、80端口的数据包

    ` tcpdump -i any -n port 80`

  - `host xxx.xxx.xxx.xxx`  指定主机地址 

    抓取 host 为192.168.171.129、端口为80 的数据

    `tcpdump -i any -n host 192.168.171.129 and port 80`

  - `-w filename`  将抓包数据保存到一个文件里

    `tcpdump -i any -n host 192.168.171.1 -w fileb`

- netstat

  `netstat -ntpl`  查看服务器监听地址

  -n 显示ip地址、不显示域名

  -t 以TCP协议截取想要显示的内容

  -p 进程

  -l  表示tcp的一个状态LISTEN

  ```cmd
  root@zyp-virtual-machine:/home/zyp/tmp# netstat -ntpl
  激活Internet连接 (仅服务器)
  Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
  tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      1394/mysqld     
  tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN      1401/redis-server 1
  tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1419/nginx -g daemo
  tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1400/sshd       
  tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2094/cupsd      
  tcp        0      0 127.0.0.1:6010          0.0.0.0:*               LISTEN      6915/8          
  tcp        0      0 127.0.0.1:6011          0.0.0.0:*               LISTEN      7113/9          
  tcp6       0      0 :::21                   :::*                    LISTEN      1365/vsftpd     
  tcp6       0      0 :::22                   :::*                    LISTEN      1400/sshd       
  tcp6       0      0 ::1:631                 :::*                    LISTEN      2094/cupsd      
  tcp6       0      0 ::1:6010                :::*                    LISTEN      6915/8          
  tcp6       0      0 ::1:6011                :::*                    LISTN      7113/9 
  ```

- ss 

  `ss -ntpl` 使用方法和 `netstat -npl` 相似。

---

#### 常用网络配置文件

网络服务管理程序分为两种：SysV、systemd

- `service network status|start|stop|restart`

- `chkconfig -list network`  如果不支持，使用 systemctl

  ```cmd
  root@zyp-virtual-machine:/# systemctl list-unit-files|grep network
  systemd-networkd-resolvconf-update.path    static  
  dbus-org.freedesktop.network1.service      disabled
  network-manager.service                    enabled 
  networking.service                         enabled 
  systemd-networkd-resolvconf-update.service static  
  systemd-networkd-wait-online.service       disabled
  systemd-networkd.service                   disabled
  systemd-networkd.socket                    disabled
  network-online.target                      static  
  network-pre.target                         static  
  network.target                             static 
  ```

- `systemctl list-unit-files NetworkManager.service`

  ```cmd
  root@zyp-virtual-machine:/# systemctl list-unit-files NetworkManager.service
  UNIT FILE              STATE  
  NetworkManager.service enabled
  ```

- `systemctl start|stop|reload|restart NetworkManager`

- `systemctl enabled|disable NetworkManger`

- `systemctl list-units` 查看活跃的单元
- `systemctl status xxx ` 查看某个xxx服务的状态
- `systemctl list-unit-files|grep enabled` 查看已启动的服务列表
- `systemctl --failed` 查看启动失败的服务列表

