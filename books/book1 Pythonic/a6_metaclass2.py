class TypeSetter(object):
    def __init__(self, fidldtype):
        self.fieldtype = fidldtype

    def is_valid(self, value):
        return isinstance(value, self.fieldtype)

class TypeCheckMeta(type):
    def __new__(cls, name, bases, dict):
        return super(TypeCheckMeta, cls).__new__(cls, name, bases, dict)

    def __init__(self, name, bases, dict):
        super(TypeCheckMeta, self).__init__(name,bases,dict)
        self._fields = {}
        for key, value in dict.items():
            if isinstance(value, TypeSetter):
                self._fields[key] = value


class TypeCheck(object):
    __metaclass__ = TypeCheckMeta
    def __setattr__(self, key, value):
        if key in self._fields:
            # ToDo:待解决AttributeError: 'MetaTest' object has no attribute '_fields'
            if not self._fields[key].is_valid(value):
                raise TypeError('Invalid type for field')
        super(TypeCheck, self).__setattr__(key, value)

class MetaTest(TypeCheck):
    name = TypeSetter(str)
    num = TypeSetter(int)

mt = MetaTest()
mt.name = 'apple'
# mt.num = 'test'



def test(cls):
    pass

