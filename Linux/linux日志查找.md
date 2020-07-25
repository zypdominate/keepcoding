#### Linux下查看日志文件

测试对象：一个名为 testfile 的文档，里面每一行是一个数字，首尾行分别是1和100。

- 查看前 20 行

  `head testfile -n 20`

- 查看最后20行

  `tail testfile -n 20`

- 查看从第20行开始往后的内容

  `tail testfile -n +20`

- 循环实时查看最后10行日志

  `tail -f 10 testfile`

- 配合 grep 使用 tail 实时查看日志

  `tail -f testfile |grep xxx` 实时查看日志最后是否出现含有xxx的内容

- 查看某范围内的某些行

  从第10行开始，显示10行。即显示10~19行

  `cat testfile |tail -n +10 |head -n 10 `

  ```shell
  root@root:/tmp# cat testfile |tail -n +10 |head -n 10 
  10
  11
  12
  13
  14
  15
  16
  17
  18
  19
  root@root:/tmp# 
  ```

  解释：`tail -n +10` 从第10行开始显示，然后`head -n 10`接着显示前面的10行。

- 合并多个文件为一个文件

  先准备两个文件 file1 和 file2

  `cat file1 file2 >file12` 

  ```shell
  root@root:/tmp# cat file1
  file1 content
  root@root:/tmp# cat file2
  file2 content
  root@root:/tmp# cat file1 file2 > file12
  root@root:/tmp# cat file12
  file1 content
  file2 content
  ```

- 将一个日志文件的内容追加到另外一个 

  `cat file3 >>file12`

  ```shell
  root@root:/tmp# cat file3
  extend content
  root@root:/tmp# cat file3 >>file12
  root@root:/tmp# cat file12
  file1 content
  file2 content
  extend content
  ```

- 反向输出行内容

  t通常的打印是从首行到末行，而 tac 打印从末行到首行

  ```shell
  root@root:/tmp# tac file12
  extend content
  file2 content
  file1 content
  ```

- 使用 sed 进行范围查找

  ```shell
root@root:/tmp# sed -n '6,10p' testfile
  6
  7
  8
  9
  10
  ```
  
- 统计文件行数

  - c 统计字节数
  - l 统计行数
  - w 统计字数

  ```shell
  root@root:/tmp# wc -clw testfile
        100       100       292 testfile
  ```

  

