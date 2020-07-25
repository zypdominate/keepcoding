class A(object):
    def __new__(cls, *args, **kwargs):
        print(cls, args, kwargs)
        instance = object.__new__(cls)
        print(instance)
        return instance
    def __init__(self, *args, **kwargs):
        self.a, self.b = args
        print(self.a, self.b)
        print(kwargs)

a1 = A(1,2,var=3)
print(a1.a)
print(a1.b)


class B(object):
    def __new__(cls, *args):
        # return object.__new__(cls)
        return super(B,cls).__new__(cls)
    def __init__(self, a, b):
        self.a = a
        self.b = b
b = B(1,2)
