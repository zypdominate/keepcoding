class A(object):
    def __init__(self):
        self._var = 0

    def get_var(self):
        return self._var

    def set_var(self, value):
        self._var = value

    def del_var(self):
        del self._var

    var = property(get_var, set_var, del_var, "A property")


a = A()

'''
a.__dict__
Out[3]: {'_var': 0}
a.var
Out[4]: 0
a.var = 1
a.var
Out[6]: 1
del a.var
a.__dict__
Out[8]: {}
'''


class B(object):
    _var = None

    def __init__(self):
        self._var = None

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, value):
        self._var = value

    @var.deleter
    def var(self):
        del self._var


class Date(object):
    def __init__(self, dateString):
        self._date = dateString

    def get_data(self):
        return self._date

    def set_data(self, dataString):
        year, month, day = dataString.split('-')
        if not (0 <= int(year) <= 3000 and 0 <= int(month) <= 12 and 0 <= int(day) <= 31):
            assert 0, f'{dataString} is invalid'
        self._date = dataString

    date = property(get_data, set_data)


date = Date('2019-10-1')
print(date.date)
date.date = '4000-10-1'
print(date.date)
