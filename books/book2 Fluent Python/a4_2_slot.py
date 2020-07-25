
class Vector2d(object):

    # 这里使用元组，因为这样定义的__slots__中所含的信息不会变化
    __slots__ = ('__x', '__y')

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

v = Vector2d(3, 4)
print(v.__slots__)
# ('__x', '__y')

# print(v.__dict__)
# AttributeError: 'Vector2d' object has no attribute '__dict__'

print(v._Vector2d__x)
# 3.0