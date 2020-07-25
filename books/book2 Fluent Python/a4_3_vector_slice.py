class Myseq:
    def __getitem__(self, index):
        return index

seq = Myseq()

print(seq[1])
# 1
print(seq[1:4])
# slice(1, 4, None)
print(seq[1:4:2])
# slice(1, 4, 2)
print(seq[1:4:2, 9])  # 如果[]中有逗号，那么__getitem__收到的是元组。
# (slice(1, 4, 2), 9)
print(seq[1:4:2, 7:9])  # 元组中甚至可以有多个切片对象。
# (slice(1, 4, 2), slice(7, 9, None))



import math
import numbers
import reprlib
from array import array


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._classname = type(self).__name__  # Vector
        self._components = array(self.typecode, components)  # array('d', [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

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
        # 这里不能像abs和bool函数里写的那样直接写self，会导致循环调用__bytes__

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])  # d b'd\x00\x00\x00\x0.....
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

    def __len__(self):
        return len(self._components)


    def __getitem__(self, index):
        cls = type(self)  # <class '__main__.Vector'>
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = f'{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))


vector = Vector(range(7))
print(repr(vector))  # Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])
print(vector)  # Vector([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
print(len(vector))  # 7
print(vector[0])  # 0.0
print(vector[1:3])  # Vector([1.0, 2.0])
print(vector.frombytes(bytes(vector)))  # Vector([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])