# 在查询的时候把非字符串的键转换为字符串

class StrKeyDict(dict):  # 继承dict
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)  # 若找不到的键本身就是字符串，抛出异常
        return self[str(key)]  # 否则，把它转换成字符串再查找

    def get(self, key, default=None):
        # 改写get方法，把查找工作用 self[key] 的形式委托给 __getitem__，
        # 好让它的表现跟__getitem__一致
        # 在查找失败前，还能通过 __missing__ 再给某个键通过self[str(key)]查找的机会
        try:
            return self[key]
        except KeyError:  # 若抛出KeyError，说明 __missing__ 也失败了，返回 default。
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()


strDict = StrKeyDict({'one': 1, 2: 2, '3': 'three'})
print(strDict[3])
print(strDict.get(4, 0))

'''
为什么 isinstance(key, str) 测试在上面的 __missing__ 中是必需的。
如果没有这个测试，只要 str(k) 返回的是一个存在的键，那么 __missing__ 方法是没问题的，
不管是字符串键还是非字符串键，它都能正常运行。但是如果 str(k) 不是一个存在的键，
代码就会陷入无限递归。这是因为 __missing__ 的最后一行中的 self[str(key)] 会调
用 __getitem__，而这个 str(key) 又不存在，于是 __missing__ 又会被调用。

为了保持一致性，__contains__ 方法在这里也是必需的。这是因为 k in d 这个操作会调用
它，但是我们从 dict 继承到的 __contains__ 方法不会在找不到键的时候调用 __missing__方法。
__contains__ 里还有个细节，就是我们这里没有用更具 Python 风格的方式——
k in my_dict——来检查键是否存在，因为那也会导致 __contains__ 被递归调用。为了避免这
一情况，这里采取了更显式的方法，直接在这个 self.keys() 里查询。

'''

# 子类化UserDict
import collections


# 无论是添加、更新还是查询操作，StrKeyDictU 都会把非字符串的键转换为字符串
class StrKeyDictU(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data  # 不必使用self.keys()

    def __setitem__(self, key, value):  # __setitem__ 会把所有的键都转换成字符串
        self.data[str(key)] = value


userDict = StrKeyDictU({'one': 1, 2: 2, '3': 'three'})
print(userDict[3])
print(userDict[2])
print(userDict.get(2))

'''
UserDict 并不是 dict 的子类，但是 UserDict 有一个叫作data 的属性，是 dict 的实例，
这个属性实际上是 UserDict 最终存储数据的地方。
这样做的好处是，比起上一个例子，UserDict 的子类就能在实现 __setitem__ 的时候避免不必要的递归，
也可以让 __contains__ 里的代码更简洁。
'''
