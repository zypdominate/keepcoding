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

---

#### iptables 的 nat 表

#### iptables 配置文件

#### firewallD 服务

省略了，用到再去搜索使用。

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

  





