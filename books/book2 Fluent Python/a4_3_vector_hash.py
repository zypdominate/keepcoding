import functools
import math
import numbers
import operator
import reprlib
from array import array


class Vector():
    type_code = 'd'
    shortcut = 'xyzw'

    def __init__(self, components):
        self._cls = type(self)
        self._classname = self._cls.__name__
        self._components = array(self.type_code, components)

    def __getattr__(self, item):
        if len(item) == 1 and item in self.shortcut:
            return self._components[self.shortcut]
        else:
            msg = f'{self._classname} object has no attribue: {item}'
            raise AttributeError(msg)

    def __setattr__(self, key, value):
        if len(key) == 1:
            if key in self._cls.shortcut:
                error = f'readonly attribute {self._classname}'
            elif key.islower():
                error = f'can\'t set attribute "a" to "z" in {self._classname}'
            else:
                error = ''
            if error:
                raise AttributeError(error)
        super().__setattr__(key, value)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'{self._classname}({components})'

    def __str__(self):
        return f'{self._classname}({list(self)})'

    def __bytes__(self):
        return (bytes([ord(self.type_code)])) + bytes(self._components)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

    def __len__(self):
        return len(self._components)

    def __eq__(self, other):
        # return tuple(self) == tuple(other)  # 对于多维向量比较太耗时、低效

        if len(self) != len(other):
            return False
        for a, b in zip(self, other):  # zip 函数生成一个由元组构成的生成器
            if a != b:
                return False
        return True

        # 使用聚合函数 all
        # return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = f'{self.cls.__name__} indices must be intergers'
            raise AttributeError(msg.format(cls=self._cls))

    def __hash__(self):
        hashed = (hash(x) for x in self._components)  # 创建生成器表达式，惰性计算各个分量的散列值。
        # hashed = map(hash, self._components)  # 把生成器表达式替换成map方法，映射过程更明显
        return functools.reduce(operator.xor, hashed, 0)


vector = Vector(range(1, 10))
print(hash(vector))
