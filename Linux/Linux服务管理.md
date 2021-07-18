[toc]

### 防火墙

#### 防火墙的分类

软件防火墙和硬件防火墙

包过滤防火墙和应用层防火墙

- CentOS 6 默认的防火墙是 iptables
- CentOS 7 默认的防火墙是 firewallD （底层使用 netfilter）

---

#### iptables 的表和链

规则表：

- filter  nat  mangle raw

规则链：

	- INPUT  OUTPUT  FORWARD
	- PREROUTING  POSTROUTING

---

#### iptables 的 filter 表

使用方法：`iptables -t filter 命令 规则链 规则`

```bash
[root@bogon home]# iptables -t filter -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     udp  --  anywhere             anywhere             udp dpt:domain
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:domain
ACCEPT     udp  --  anywhere             anywhere             udp dpt:bootps
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:bootps

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
DOCKER-USER  all  --  anywhere             anywhere            
DOCKER-ISOLATION-STAGE-1  all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
DOCKER     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
DOCKER     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             bogon/24             ctstate RELATED,ESTABLISHED
ACCEPT     all  --  bogon/24             anywhere            
ACCEPT     all  --  anywhere             anywhere            
REJECT     all  --  anywhere             anywhere             reject-with icmp-port-unreachable
REJECT     all  --  anywhere             anywhere             reject-with icmp-port-unreachable

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     udp  --  anywhere             anywhere             udp dpt:bootpc       
```

```bash
iptables -t filter -A INPUT -s 10.103.131.241 -j ACCEPT   # 添加某ip
iptables -t filter -A INPUT -s 10.103.131.0/241 -j ACCEPT   # 添加某一段ip
iptables -t filter -nL
```

添加命令的先后顺序，影响命令的优先级

```bash
iptables -t filter -A INPUT -s 10.103.131.241 -j ACCEPT
iptables -t filter -A INPUT -s 10.103.131.241 -j DROP
```

上面这种情况下， 依然可以接收 10.103.131.241，因为 ACCEPT 在 DROP 前面。

```bash
iptables -t filter -I INPUT -s 10.103.131.243 -j DROP   # 将此条插入到最前面
```

删除添加的规则：

```bash
iptables -t filter -D INPUT -s 10.103.131.241 -j ACCEPT   # 删除
```

更改 policy：

```bash
iptables -P INPUT DROP   # 将input规则改为drop
iptables -P INPUT ACCEPT   # 将上一条改的改回去
```

`iptables 的 nat 表，iptables 配置文件，firewallD 服务`  省略了，用到再去搜索使用。

---

### SSH相关

#### Telnet

安装 telnet：`yum install telnet telnet-server xinetd -y`

启动：

```bash
systemctl start xinetd.service
systemctl start telnet.socket
```

登录：

```
telnet xxx.xxx.xxx.xxx
```

#### SSH 命令

- systemctl status | start | stop | restart | enable | disable sshd.service
- 客户端命令
  - ssh [-p 端口] 用户@远程ip
  - SecureCRT
  - Xshell
  - putty

#### SSH公钥认证

常用命令：

- 客户端产生秘钥：ssh-keygen -t rsa  

- ssh-copy-id  （命令可能报错的解决方法：`yum -y install openssh-clients`）

  将客户端的公钥传到服务端：` ssh-copy-id -i /Users/foxit/.ssh/id_rsa.pub root@10.xxx.xxx.242`

  或者 `cat /Users/foxit/.ssh/id_rsa.pub |ssh root@10.xxx.xxx.242 'cat >> .ssh/authorized_keys'`

- 其他使用拷贝方法

  ```bash
  # 将本地文件拷贝到远程主机
  Mac:~ foxit$ scp test.txt root@10.xxx.xxx.242:/root/Desktop
  test.txt                                    100%   12     0.0KB/s   00:00 
  ```

  ```bash
  # 将远程主机文件拷贝到本地
  Mac:~ foxit$ scp root@10.103.131.242:/root/Desktop/test.txt ./new_test.txt
  test.txt                                    100%   12     0.0KB/s   00:00    
  ```

---

### 文件服务

#### FTP  vsftpd 服务

安装：`yum install vsftpd ftp`

启动：`systemctl [enable] start vsftpd.service`

建议将 selinux 改为 permissive：

- `getsebool -a |grep ftpd`
- `setsebool -P <sebool> 1`

---

#### samba 服务

安装：`yum install samba`

配置文件：

`/etc/samba/smb.conf`

```
[share]
	comment=my_share
	path=/data/share
	read only=No
```

用户的设置：

- smbpasswd命令： -a  添加用户；  -x  删除用户

  ```
  useradd use1
  smbpasswd -a user1
  pdbedit -L
  ```

- pdbedit：-L 查看用户

服务的启动：

`systemctl start| stop smb.service`

- Linux 客户端挂载服务器共享的目录
  - `mount -t cifs -o username=user1 //127.0.0.1/user1 /mnt`
  - `umount /mnt`

- Windows客户端
  - 资源管理器访问共享
  - 映射网络驱动器

---

Ubuntu 上设置共享目录

安装：`apt-get install samba samba-client samba-common`

修改配置：`vi /etc/samba/smb.conf`

```
[global]
        workgroup = SAMBA
        map to guest = bad user
username map = /etc/samba/smbusers
encrypt passwords = true
passdb backend = smbpasswd
smb passwd file =/etc/samba/smbpasswd
        printing = cups
        printcap name = cups
        load printers = yes
        cups options = raw
[homes]
        comment = Home Directories
        valid users = %S, %D%w%S
        browseable = No
        read only = No
        inherit acls = Yes
[printers]
        comment = All Printers
        path = /var/tmp
        printable = Yes
        create mask = 0600
        browseable = No
[print$]
        comment = Printer Drivers
        path = /var/lib/samba/drivers
        write list = root
        create mask = 0664
        directory mask = 0775
[share]
        comment = share
        path = /data/share   # 这是我要共享linux机子上的目录，需要存在这个目录
        available = Yes
        browseable = Yes
        public = Yes
        writable = Yes
        printable = No
```

启动：`service smb start` 或者 `systemctl restart smb.service`

参考：Linux[设置共享文件夹](https://blog.csdn.net/qq_35573326/article/details/103732944?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-6.control&dist_request_id=1329188.9156.16178529985492373&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-6.control)，Samba[配置流程](https://blog.csdn.net/dingyanxxx/article/details/47205997)，samba[的安装与配置](https://www.cnblogs.com/jfyl1573/p/6514634.html)

---

#### nfs 服务

- `/etc/exports`

  `/data/share *(re, sync, all_squash)`

- `showmount -e localhost`

- 客户端使用挂载方式访问

  `mount -t nfs localhost:/data/share /ent`

- 启动 nfs 服务

  `systemctl  start|stop nfs.service`

