# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:
@time:2020/3/26
"""
import keyword
from collections import abc


class FrozenJSON():
    '''
    一个只读接口，使用属性表示法访问JSON类对象
    '''

    def __init__(self, mapping):
        self._data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):  # 处理无效属性名
                key += '_'
            self._data[key] = value

    def __getattr__(self, name):
        if hasattr(self._data, name):
            print("hasattr:", name)
            return getattr(self._data, name)
        else:
            if keyword.iskeyword(name):
                name += '_'
            return FrozenJSON.build(self._data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


if __name__ == '__main__':
    from a6_1_dynamic_attr import load2

    raw_data = load2()
    data = FrozenJSON(raw_data)

    print(len(data.Schedule.speakers))

    print(sorted(data.Schedule.keys()))

    for key, value in sorted(data.Schedule.items()):
        print('{:3}:{}'.format(len(value), key))

    # data.Schedule.speakers，仍是列表；但是，如果里面的元素是映射，会转换成FrozenJSON对象。
    talk = data.Schedule.events[40]  # events列表中的40号元素是一个JSON对象，现在则变成一个FrozenJSON实例。
    print(type(talk))
    print(talk.name)
    print(talk.speakers)
    try:
        print(talk.flavor)
    except Exception as e:
        print(e)
    # print(talk.flavor)

    # 对于有无效属性名的情况:
    grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
    print(getattr(grad, 'class'))
    print(grad.class_)
