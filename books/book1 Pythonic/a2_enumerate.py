# 对某一序列进行迭代并获取序列中的元素进行处理
list_ = [1, '2', True, None, 8]

# way1
index1 = 0
for i in list_:
    print(f"index:{index1}, i:{i}")
    index1 += 1

# way2
for i in range(len(list_)):
    print(f"i:{i}, element:{list_[i]}")

# way3
index3 = 0
while index3 < len(list_):
    print(f"index:{index3}, element:{list_[index3]}")
    index3 += 1

# way4
for i, ele in zip(range(len(list_)), list_):
    print(f"i:{i}, element:{ele}")

# way5:
for i, ele in enumerate(list_):
    print(f"i:{i}, element:{ele}")

# 推荐 enumerate(sequence,start=0)
# sequence可以是任何可迭代对象，函数返回本质上是一个迭代器，可用next()获取下一个迭代元素
enu = enumerate(list_)
next(enu)  # (0, 1)

# enumerate内部实现原理
def mock_enumerate(sequence, start=0):
    n = start
    for ele in sequence:
        yield n, ele
        n += 1

# 实现自己的enumerate()函数：反序列
def reverse_enumerate(sequence, start=0):
    n = -1
    for ele in reversed(sequence):
        yield len(sequence)+n, ele
        n -= 1

# 对于字典的迭代，enumerate()并不适合，而是应该使用方法items()
mydict = {1:'aa',2:'bb'}
for key,value in mydict.items():
    print(key,value)