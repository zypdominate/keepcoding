from array import array
from random import random

floats_array = array('d', (random() for i in range(10 ** 7)))  # 双精度浮点数组，类型码:d
print(floats_array[0])

f = open('floats.bin', 'wb')
floats_array.tofile(f)  # 把数组存入一个二进制文件中
f.close()

floats_array2 = array('d')  # 新建一个双精度浮点空数组
f = open('floats.bin', 'rb')
floats_array2.fromfile(f, 10 ** 7) # 把10**7个浮点数从二进制文件中读取出来
f.close()
print(floats_array2[0])
print(floats_array == floats_array2)  # 检查两个数组是否相同
