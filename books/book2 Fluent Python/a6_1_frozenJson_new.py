import keyword
from collections import abc


class FrozenJSON():
    def __new__(cls, arg):
        print(arg)
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self._data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self._data[key] = value

    def __getattr__(self, name):
        if hasattr(self._data, name):
            return getattr(self._data, name)
        else:
            if keyword.iskeyword(name):
                name += '_'
            return FrozenJSON(self._data[name])


if __name__ == '__main__':

    grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
    print(getattr(grad, 'class'))
    print(grad.class_)
