def update_meta(self, other):
    self.__name__ = other.__name__
    self.__doc__ = other.__doc__
    self.__dict__.update(other.__dict__)
    return self

class MyProperty(property):
    # def __new__(cls, *args, **kwargs):
    def __new__(cls, fget=None, fset=None, fdel=None, doc=None):
        if fget is not None:
            def __get__(obj, objtype=None, name=fget.__name__):
                fget = getattr(obj, name)
                print(f'fget:{fget.__name__}')  # fget:get
                print(f'{obj},{obj.__dict__}')  # <__main__.A object at 0x0000029346BAB400>,{'_x': 1}
                return fget()
            fget = update_meta(__get__, fget)

        if fset is not None:
            def __set__(obj, value, name=fset.__name__):
                fset = getattr(obj, name)
                return fset(value)
            fset = update_meta(__set__, fset)

        if fdel is not None:
            def __delete__(obj, name=fdel.__name__):
                fdel = getattr(obj,name)
                return fdel()
            fdel = update_meta(__delete__, fdel)
        return property(fget, fset, fdel, doc)

class A(object):
    def get(self):
        return self._x
    def set(self, x):
        self._x = x
    def delete(self):
        del self._x
    x = MyProperty(get,set,delete)

a = A()
print(a.__dict__)
a.x = 1
print(a.x)
del a.x
print(a.__dict__)


