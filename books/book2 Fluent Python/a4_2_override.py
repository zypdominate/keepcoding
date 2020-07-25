class Vector2d(object):
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

v = Vector2d(3, 4)
print(v.typecode)  # d

v.typecode = 'f'
print(v.typecode)   # f
print(Vector2d.typecode)  # d

Vector2d.typecode = 'e'
print(Vector2d.typecode)
print(v.typecode)   # f



from a4_2_vector2d import Vector2d

class ShortVector2d(Vector2d):
    typecode = 's'

sv = ShortVector2d(1,2)
print(sv)  # str：ShortVector2d(1.0, 2.0)
print(sv.typecode)  # s



class Demo():
    @classmethod
    def cls_method(*args):
        return args

    @staticmethod
    def static_method(*args):
        return args

print(Demo.cls_method())  # (<class '__main__.Demo'>,)
print(Demo.cls_method('a'))  # (<class '__main__.Demo'>, 'a')

print(Demo.static_method())  # ()
print(Demo.static_method('b'))  # ('b',)
