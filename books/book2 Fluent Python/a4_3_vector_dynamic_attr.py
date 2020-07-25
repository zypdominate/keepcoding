import math
import numbers
import reprlib
from array import array


class Vector:
    typecode = 'd'
    shortcut_name = 'xyzw'

    def __init__(self, components):
        self.cls = type(self)  # <class '__main__.Vector'>
        self._classname = self.cls.__name__  # Vector
        self._components = array(self.typecode, components)  # array('d', [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

    # 属性查找失败后，解释器会调用 __getattr__ 方法
    def __getattr__(self, item):
        if len(item) == 1 and item in self.shortcut_name:
            return self._components[self.shortcut_name.index(item)]
        # if len(item) == 1:
        #     index = self.cls.shortcut_name.find(item)
        #     if 0 <= index < len(self._components):
        #         return self._components[index]
        else:
            msg = f'{self._classname} object has no attribute: {item}'
            raise AttributeError(msg)

    def __setattr__(self, key, value):
        if len(key) == 1:  # 这里只特别处理名称是单个字符的属性
            if key in self.cls.shortcut_name:
                error = f'readonly attribute {self._classname}'
            elif key.islower():
                error = f'can\'t set attrbute "a" to "z" in {self._classname}'
            else:
                error = ''
            if error:
                raise AttributeError(error)
        super().__setattr__(key, value)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)  # "array('d', [1.0, 2.0, 3.0, 4.0, 5.0, ...])"
        components = components[components.find('['):-1]
        return f'{self._classname}({components})'

    def __str__(self):
        return f'{self._classname}({list(self)})'

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

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

    def __getitem__(self, index):

        if isinstance(index, slice):
            return self.cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = f'{self.cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=self.cls))


vector = Vector(range(1, 7))

# print(vector.a)  # AttributeError: Vector object has no attribute: a
print(vector.x)  # 1.0
vector.x = 10  # AttributeError: readonly attribute Vector
# vector.a = 10  # AttributeError: can't set attrbute "a" to "z" in Vector
# vector.A = 10
# print(vector.A)  # 10
