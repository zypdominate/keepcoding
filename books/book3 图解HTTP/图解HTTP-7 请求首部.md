[toc]

请求首部字段：存在于客户端发往服务器端的请求报文，用于补充请求的附加信息、客户端信息、对响应内容相关的优先级等内容。

## Accept

Accept首部字段可通知服务器，用户代理能够处理的**媒体类型**及媒体类型的相对优先级。可使用type/subtype这种形式，一次指定多种媒体类型。

常见的媒体类型：

-  文本文件

  text/html, text/plain, text/css ...

  application/xhtml+xml, application/xml ...

- 图片文件

  image/jpeg, image/gif, image/png ...

- 视频文件

  video/mpeg, video/quicktime ...

- 应用程序使用的二进制文件

  application/octet-stream, application/zip ...

若想要给显示的媒体类型增加优先级，则使用q=来额外表示权重值，用分号（;）进行分隔。权重值q的范围是0～1（可精确到小数点后3位），且1为最大值。不指定权重q值时，默认权重为q=1.0。

当服务器提供多种内容时，将会首先返回权重值最高的媒体类型。

示例：

```
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
```

---

## Accept-Charset

用于通知服务器用户代理支持的**字符集**及字符集的相对优先顺序。

示例：

```
Accept-Charset: iso-8859-5, unicode-1-1;q=0.8
```

---

## Accept-Encodeing

告知服务器用户代理支持的**内容编码**及内容编码的优先级顺序。可一次性指定多种内容编码。也可使用星号（*）作为通配符，指定任意的编码格式。

场景内容编码：

- gzip

  由文件压缩程序gzip（GNU zip）生成的编码格式（RFC1952）

- compress

  由UNIX文件压缩程序compress生成的编码格式

- deflate

  组合使用zlib格式（RFC1950）及由deflate压缩算法（RFC1951）生成的编码格式

- identity

  不执行压缩或不会变化的默认编码格式

示例：

```
Accept-Encoding: gzip, deflate
```

---

## Accept-Language

告知服务器用户代理能够处理的**自然语言集**（指中文或英文等），以及自然语言集的相对优先级。可一次指定多种自然语言集。

如下示例：客户端在服务器有中文版资源的情况下，会请求其返回中文版对应的响应，没有中文版时，则请求返回英文版响应。

```
Accept-Language: zh-ch,zh;q=0.7,en-us,en;q=0.3
```

---

## Authorization

告知服务器，用户代理的**认证信息**（证书值）。

通常，想要通过服务器认证的用户代理会在接收到返回的401状态码响应后，把首部字段Authorization加入请求中。

---

## Expect

客户端使用首部字段Expect来告知服务器，**期望出现的某种特定行为**。因服务器无法理解客户端的期望作出回应而发生错误时，会返回状态码417 ExpectationFailed。

客户端可以利用该首部字段，写明所期望的扩展。虽然HTTP/1.1规范只定义了100-continue（状态码100 Continue之意）。

---

## From

告知服务器使用用户代理的用户的电子邮件地址。通常，其使用目的就是为了显示搜索引擎等用户代理的负责人的电子邮件联系方式。

通常，其使用目的就是为了显示搜索引擎等用户代理的负责人的电子邮件联系方式。

---

## Host

首部字段Host会告知服务器，请求的资源所处的互联网主机名和端口号。**Host首部字段在HTTP/1.1规范内是唯一一个必须被包含在请求内的首部字段。**

请求被发送至服务器时，请求中的主机名会用IP地址直接替换解决。但如果这时，相同的IP地址下部署运行着多个域名，那么服务器就会无法理解究竟是哪个域名对应的请求。因此，就需要使用首部字段Host来明确指出请求的主机名。若服务器未设定主机名，那直接发送一个空值即可。

---

## If-xxx

形如 `If-xxx` 这种样式的请求首部字段，都可称为**条件请求**。服务器接收到附带条件的请求后，只有判断指定条件为真时，才会执行请求。

#### If-Match

告知服务器匹配资源所用的实体标记（ETag）值。

服务器比对`If-Match`的字段值和资源的`ETag`值，仅当两者一致时，才会执行请求。反之，则返回状态码`412 Precondition Failed`的响应。

#### If-Modified-Since

用于确认代理或客户端拥有的本地资源的有效性。

告知服务器若`If-Modified-Since`字段值早于资源的更新时间，则希望能处理该请求。而在指定`If-Modified-Since`字段值的日期时间之后，如果请求的资源都没有过更新，则返回状态码`304 Not Modified`的响应。

#### If-Unmodified-Since

和首部字段`If-Modified-Since`的作用相反。它的作用的是告知服务器，指定的请求资源只有在字段值内指定的日期时间之后，未发生更新的情况下，才能处理请求。如果在指定日期时间后发生了更新，则以状态码`412 Precondition Failed`作为响应返回。

#### If-None-Match

与`If-Match`作用相反。用于指定`If-None-Match`字段值的实体标记（ETag）值与请求资源的ETag不一致时，它就告知服务器处理该请求。

在GET或HEAD方法中使用首部字段`If-None-Match`可获取最新的资源。因此，这与使用首部字段`If-Modified-Since`时有些类似。

#### If-Range

首部字段`If-Range`属于附带条件之一。它告知服务器若指定的`If-Range`字段值（ETag值或者时间）和请求资源的ETag值或时间相一致时，则作为范围请求处理。反之，则返回全体资源。

#### Range

对于只需获取**部分资源的范围请求**，包含首部字段Range即可告知服务器资源的指定范围。示例表示请求获取从第5001字节至第10000字节的资源：

```
Range: bytes=5001-10000
```

接收到附带Range首部字段请求的服务器，会在处理请求之后返回状态码为`206 Partial Content`的响应。无法处理该范围请求时，则会返回状态码`200 OK`的响应及全部资源。

#### Max-Forwards

通过TRACE方法或OPTIONS方法，发送包含首部字段`Max-Forwards`的请求时，该字段以十进制整数形式指定可经过的服务器最大数目。服务器在往下一个服务器转发请求之前，会将`Max-Forwards`的值减1后重新赋值。当服务器接收到`Max-Forwards`值为0的请求时，则不再进行转发，而是直接返回响应。

#### Proxy-Authorization

接收到从代理服务器发来的认证质询时，客户端会发送包含首部字段`Proxy-Authorization`的请求，以告知服务器认证所需要的信息。

#### Referer

告知服务器请求的原始资源的URI。

#### TE

告知服务器客户端能够处理响应的**传输编码方式**及相对优先级。它和首部字段`Accept-Encoding`的功能很相像，但是用于传输编码。

首部字段TE除指定传输编码之外，还可以指定伴随trailer字段的分块传输编码的方式。应用后者时，只需把trailers赋值给该字段值。

#### User-Agent

首部字段User-Agent会将创建请求的浏览器和用户代理名称等信息传达给服务器。

```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
```

