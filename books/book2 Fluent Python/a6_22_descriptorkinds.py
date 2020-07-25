def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    # print(cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return f'<class {obj.__name__}>'
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return f'<{cls_name(obj)} object>'


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print(f'-> {cls_name(args[0])}.__{name}__({pseudo_args})')


class Overriding:
    """数据描述符/强制描述符"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    """没有__get__方法的覆盖型描述符"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:
    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    # 托管类：使用各个描述符的一个实例
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):
        # spam方法放在这里是为了对比，因为方法也是描述符。
        print(f'-> Managed.spam({display(self)})')


if __name__ == '__main__':

    obj = Managed()
    # obj.over
    # # -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    # Managed.over
    # # -> Overriding.__get__(<Overriding object>, None, <class Managed>)
    # obj.over = 1
    # # -> Overriding.__set__(<Overriding object>, <Managed object>, 1)
    # obj.over
    # # -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    # obj.__dict__['over'] = 8
    # print(vars(obj))
    # # {'over': 8}
    # obj.over
    # # -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)

    # print(obj.over_no_get)
    # # <__main__.OverridingNoGet object at 0x000001E072A18BA8>
    # print(Managed.over_no_get)
    # # <__main__.OverridingNoGet object at 0x000001E072A18BA8>
    # obj.over_no_get = 1
    # # -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 1)
    # print(obj.over_no_get)
    # # <__main__.OverridingNoGet object at 0x000001E072A18BA8>
    # obj.__dict__['over_no_get'] = 2
    # print(obj.over_no_get)  # 2
    # obj.over_no_get = 3
    # # -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 3)
    # print(obj.over_no_get)  # 2

    # obj.non_over
    # # -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
    # obj.non_over = 1
    # print(obj.non_over)  # 1
    # Managed.non_over
    # # -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)
    # del obj.non_over
    # obj.non_over
    # # -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)

    # Managed.over = 1
    # Managed.over_no_get = 2
    # Managed.non_over = 3
    # print(obj.over, obj.over_no_get, obj.non_over)
    # 1 2 3

    print(obj.spam)
    # <bound method Managed.spam of <__main__.Managed object at 0x000001C5275EBC50>>
    print(Managed.spam)
    # <function Managed.spam at 0x000001C52761E6A8>
    obj.spam = 1
    print(obj.spam)  # 1
