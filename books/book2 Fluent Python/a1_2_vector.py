from math import hypot


class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):     # 把对象用字符串的形式表达出来
        return f'Vector: {self.x},{self.y}'

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        # return bool(self.__abs__())
        return bool(abs(self))

    # def __bool__(self):
    #     return bool(self.x or self.y)  # 更高效的bool实现方式

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

v1 = Vector(1, 2)
v2 = Vector(2, 3)


'''
通过 __add__ 和 __mul__，示例为向量类带来了 + 和 * 这两个算术运算符。
值得注意的是，这两个方法的返回值都是新创建的向量对象，
被操作的两个向量（self 或 other）还是原封不动，代码里只是读取了它们的值而已。
中缀运算符的基本原则就是不改变操作对象，而是产出一个新的值。
'''