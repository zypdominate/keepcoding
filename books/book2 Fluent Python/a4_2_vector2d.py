import math
from array import array


class Vector2d(object):
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        # 没有硬编码class_name的值，而是使用type(self).__name__获取
        self.class_name = type(self).__name__

    def __iter__(self):  # TypeError: 'Vector2d' object is not iterable
        return (i for i in (self.x, self.y))  # a, b = v

    def __str__(self):
        return f"str：{self.class_name}" + str(tuple(self))  # print(v)

    def __format__(self, format_spec=''):
        components = (format(item, format_spec) for item in self)
        return '({}, {})'.format(*components)

    def __repr__(self):
        return f'repr：{self.class_name}({self.x},{self.y})'  # repr(v)
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

if __name__ == '__main__':

    v = Vector2d(3, 4)
    # print(v.x, v.y)  # 3 4
    # print(v())  # str:(3.0, 4.0)

    a, b = v
    # print(a, b)  # 3 4

    # print 函数会调用 str 函数
    # print(v)   # str:(3, 4)

    # 在控制台输入 v 的效果：
    # repr函数调用Vector2d实例，得到的结果类似于构建实例的源码。
    # 相当于以下代码：
    print(repr(v))  # Vector2d(3,4)
    # print(type(repr(v)))  # <class 'str'>


    # 使用eval函数，表明repr函数调用 Vector2d 实例得到的是对构造方法的准确表述
    v_clone = eval(repr(v))
    print(type(v_clone))  # <class '__main__.Vector2d'>
    print(v_clone)  # str:(3, 4)
    print(v_clone.x)  # 3
    print(v_clone.y)  # 4

    print(v == v_clone)  # True
    print(v is v_clone)  # False

    print(bytes(v))  # b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'

    print(abs(v))  # 5.0

    print(format(v))
    print(format(v, '.3f'))
    print(format(v, '.3e'))
