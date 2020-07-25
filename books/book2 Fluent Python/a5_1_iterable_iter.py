s = "abc"
for i in s:
    print(i)

s_iter = iter(s)
while True:
    try:
        print(next(s_iter))
    except StopIteration:
        del s_iter
        break

# 检查对象 x 是否为迭代器最好的方式是调用 isinstance(x,  abc.Iterator)。
from collections import abc

print(isinstance(iter(s), abc.Iterable))  # True
print(isinstance(iter(s), abc.Iterator))  # True
