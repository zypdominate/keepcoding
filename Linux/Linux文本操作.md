[Toc]

### 元字符介绍

- `.` 匹配除换行符外的任意单个字符
- `*` 匹配任意一个跟在它前面的字符
- `[ ]` 匹配方括号中的字符类中的任意一个
- `^` 匹配开头
- `$` 匹配结尾
- `\` 转义后面的特殊字符

```shell
[root@bogon /]# grep password /root/anaconda-ks.cfg 
# Root password
user --groups=wheel --name=admin --password=$6$vhG.R4XYP2HrYqam$rsm2Ogj4Dl5lZ7aQVnS9r3KY4dbg2q4CrWjFHFAMP21/Ouc1ml.o4ko5Iy6iXKTuu/STMzJdFWsOVtgARoY2V0 --iscrypted --gecos="admin"

[root@bogon /]# grep pass.... /root/anaconda-ks.cfg 
auth --enableshadow --passalgo=sha512
# Root password
user --groups=wheel --name=admin --password=$6$vhG.R4XYP2HrYqam$rsm2Ogj4Dl5lZ7aQVnS9r3KY4dbg2q4CrWjFHFAMP21/Ouc1ml.o4ko5Iy6iXKTuu/STMzJdFWsOVtgARoY2V0 --iscrypted --gecos="admin"

[root@bogon /]# grep pass* /root/anaconda-ks.cfg 
auth --enableshadow --passalgo=sha512
# Root password
user --groups=wheel --name=admin --password=$6$vhG.R4XYP2HrYqam$rsm2Ogj4Dl5lZ7aQVnS9r3KY4dbg2q4CrWjFHFAMP21/Ouc1ml.o4ko5Iy6iXKTuu/STMzJdFWsOVtgARoY2V0 --iscrypted --gecos="admin"
```

```shell
[root@bogon /]# grep [P]assword /root/anaconda-ks.cfg 
[root@bogon /]# grep [Pp]assword /root/anaconda-ks.cfg 
# Root password
user --groups=wheel --name=admin --password=$6$vhG.R4XYP2HrYqam$rsm2Ogj4Dl5lZ7aQVnS9r3KY4dbg2q4CrWjFHFAMP21/Ouc1ml.o4ko5Iy6iXKTuu/STMzJdFWsOVtgARoY2V0 --iscrypted --gecos="admin"

[root@bogon /]# grep ^# /root/anaconda-ks.cfg 
#version=DEVEL
# System authorization information
# Use CDROM installation media
# Use graphical install
# Run the Setup Agent on first boot
# Keyboard layouts
# System language
# Network information
# Root password
# System services
# System timezone
# X Window System configuration information
# System bootloader configuration
# Partition clearing information
```

```shell
[root@bogon /]# grep "\." /root/anaconda-ks.cfg 
lang en_US.UTF-8
network  --hostname=localhost.localdomain
rootpw --iscrypted $6$mMkZah4XfneVRKWc$3QFOR6QXBfNIg1L4fFcCpw.rCXg5sUYnjUxOdBxO9V1cWBSQVvFSlRncHGiO/wsDxb7cb5Mmx5VccWGkDr4yU0
user --groups=wheel --name=admin --password=$6$vhG.R4XYP2HrYqam$rsm2Ogj4Dl5lZ7aQVnS9r3KY4dbg2q4CrWjFHFAMP21/Ouc1ml.o4ko5Iy6iXKTuu/STMzJdFWsOVtgARoY2V0 --iscrypted --gecos="admin"
```

拓展字符

- `+` 匹配前面的正则表达式至少出现一次
- `?` 匹配前面的正则表达式出现零次或一次
- `|` 匹配它前面或后面的正则表达式

---

### find 演示

```shell
[root@bogon etc]# find passwd
passwd
[root@bogon etc]# find passwd*
passwd
passwd-
[root@bogon etc]# find /etc -name passwd
/etc/passwd
/etc/pam.d/passwd
```

```shell
[root@bogon etc]# find /etc -regex .*wd
/etc/passwd
/etc/pam.d/passwd
/etc/security/opasswd
/etc/samba/smbpasswd

[root@bogon etc]# find /etc -regex .etc.*wd$
/etc/passwd
/etc/pam.d/passwd
/etc/security/opasswd
/etc/samba/smbpasswd
```

```shell
[root@bogon tmp]# touch /tmp/{1..9}.txt

[root@bogon tmp]# find *txt -exec rm -v {} \;
removed ‘1.txt’
removed ‘2.txt’
removed ‘3.txt’
removed ‘4.txt’
removed ‘5.txt’
removed ‘6.txt’
removed ‘7.txt’
removed ‘8.txt’
removed ‘9.txt’
```

```shell
[root@bogon tmp]# grep pass /root/anaconda-ks.cfg 
auth --enableshadow --passalgo=sha512
# Root password

[root@bogon tmp]# grep pass /root/anaconda-ks.cfg |cut -d " " -f 1
auth
#
[root@bogon tmp]# grep pass /root/anaconda-ks.cfg |cut -d " " -f 2
--enableshadow
Root
[root@bogon tmp]# grep pass /root/anaconda-ks.cfg |cut -d " " -f 3
--passalgo=sha512
password
```

---

### sed 和 awk

- sed 一般用于对文本内容做替换
  - `sed '/user1/s/user1/u1/'  /etc/passwd`

- awk 一般用于对文本内容进行统计、按需要的格式进行输出
  - cut 命令：`cut -d:-f 1 /etc/passwd`
  - awk 命令：`awk -F: '/wd$/{print $1}' /etc/passwd`

#### sed

sed 的基本工作方式

- 将文件以行为单元读取到内存（模式空间）
- 使用 sed 的每个脚本对该行进行操作
- 处理完成后输出该行  

#### awk

AWK 是一种处理文本文件的语言，是一个强大的文本分析工具

[Linux awk 命令 | 菜鸟教程 (runoob.com)](https://www.runoob.com/linux/linux-comm-awk.html)

