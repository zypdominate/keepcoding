def dynamic_class(name):
    if name == 'A':
        class A(object):
            pass
        return A
    elif name == 'B':
        class B(object):
            pass
        return B


MyClass = dynamic_class("A")
print(MyClass())  # <__main__.dynamic_class.<locals>.A object at 0x000001EB066CA518>
print(MyClass)  # <class '__main__.dynamic_class.<locals>.A'>
print(MyClass.__class__)  # <class 'type'>
print(MyClass().__class__)  # <class '__main__.dynamic_class.<locals>.A'>
print(MyClass.__bases__)  # (<class 'object'>,)


