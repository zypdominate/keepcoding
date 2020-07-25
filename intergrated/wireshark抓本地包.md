 学习wireshark抓包时，想把本机既作为客户端又作为服务器端来抓包测试，使得本机自己和自己通信。但由于WireShark只能抓取经过电脑网卡的包，由于我是使`ping 本地ip`来测试的，数据包不经过电脑网卡，所以WireShark无法抓包，需要配置。 

首先使用管理员身份打开cmd，ipconfig查看本地的ip：

![1568515454524](../../markdown_pic/4.wireshark抓包.png)

再通过`route add 本地ip mask 255.255.255.255 网关ip`添加路由（测试完最后再删除）：

![1568515129847](../../markdown_pic/4.wireshark抓包2.png)

然后一直ping着本地ip，制造数据包：

![1568515237796](../../markdown_pic/4.wireshark抓包3.png)

打开wireshark，抓包就可看到满屏的我在本地ping的数据包了：

![1568515373157](../../markdown_pic/4.wireshark抓包4.png)

最后，在测试完之后，使用`route add 本地ip mask 255.255.255.255 网关ip`删除添加的路由，否则我们本机的所有报文都会先经过网卡再回到本机，消耗性能。

