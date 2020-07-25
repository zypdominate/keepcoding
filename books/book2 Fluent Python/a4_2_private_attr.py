
class Vector2d(object):

    def __init__(self, x, y):
        self.__x = float(x)  # 属性标记为私有的
        self.__y = float(y)

v = Vector2d(3, 4)
print(v.__dict__)
# {'_Vector2d__x': 3.0, '_Vector2d__y': 4.0}

print(v._Vector2d__x)
# 3.0