import math
from array import array


class Vector2d(object):
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)  # 属性标记为私有的
        self.__y = float(y)

    @property  # @property 装饰器把读值方法标记为特性
    def x(self):  # 读值方法与公开属性同名，都是 x
        return self.__x

    @property
    def y(self):
        return self.__y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)  # 异或

    # 需要读取x和y分量的方法可保持不变，通过self.x和self.y读取公开特性，不必读取私有属性
    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __str__(self):
        return "str:" + str(tuple(self))  # print(v)

    def __format__(self, format_spec=''):
        components = (format(item, format_spec) for item in self)
        return '({}, {})'.format(*components)

    def __repr__(self):
        class_name = type(self).__name__
        return f'{class_name}({self.x},{self.y})'  # repr(v)
        # return '{}({!r},{!r})'.format(class_name, *self)  # repr(v)
        # return f'repr:{class_name}({self.x},{self.y})'  # repr(v)

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __call__(self, *args, **kwargs):
        return self


v = Vector2d(3, 4)
print(v.x, v.y)
# v.x = 10  # AttributeError: can't set attribute
# print(v.x)

v1 = Vector2d(3, 4)
v2 = Vector2d(3.1, 4.1)
print(hash(v1))  # 7
print(hash(v2))  # 1031
