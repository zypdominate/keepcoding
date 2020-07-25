import math
import reprlib
from array import array


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._classname = type(self).__name__
        self._components = array(self.typecode, components)  # array('d', [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)  # "array('d', [1.0, 2.0, 3.0, 4.0, 5.0, ...])"
        components = components[components.find('['):-1]
        return f'{self._classname}({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))
        # 这里不能像abs和bool函数里写的那样直接写self，会导致循环调用__bytes__

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        return self._components[index]

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])  # d b'd\x00\x00\x00\x0.....
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

vector = Vector(range(7))
print(repr(vector))  # Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])
print(vector)  # (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
print(len(vector))  # 7
print(vector[0])  # 0.0
print(vector[1:3])  # array('d', [1.0, 2.0])
print(vector.frombytes(bytes(vector)))  # (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
