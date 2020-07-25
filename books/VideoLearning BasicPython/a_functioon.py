import time
import functools

class DelayFunc:
    def __init__(self,  duration, func):
        self.duration = duration
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f'Wait for {self.duration} seconds...')
        time.sleep(self.duration)
        return self.func(*args, **kwargs)

    def eager_call(self, *args, **kwargs):
        print('Call without delay')
        return self.func(*args, **kwargs)

def delay(duration):
    """
    装饰器：推迟某个函数的执行。
    同时提供 .eager_call 方法立即执行
    """
    # 此处为了避免定义额外函数，
    # 直接使用 functools.partial 帮助构造 DelayFunc 实例
    return functools.partial(DelayFunc, duration)

@delay(duration=2)
def add(a, b):
    return a+b
# print(add)    # <__main__.DelayFunc object at 0x000001EED91FA3C8>
# print(add.eager_call(1,2))
# print(add(3, 5))

instances = {}

def singleton(cls):
    def get_instance(*args, **kwargs):
        cls_name = cls.__name__
        print("cls_name:",cls_name)
        if not cls_name in instances:
            print(f"cle_name[{cls_name}] not in instances")
            instance = cls(*args, **kwargs)
            instances[cls_name] = instance
        return instances[cls_name]
    return get_instance

@singleton
class User:
    _instance = None

    def __init__(self, name):
        self.name = name
        print("name=",self.name)

u1 =User("usr1")
print(u1,u1.name)

u2 =User("usr2")
print(u2,u2.name)

print(u1 == u2)

from functools import wraps


