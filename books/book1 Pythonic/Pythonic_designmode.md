**Rome was not built in one day， coding will not advance vigorously with one effort.**

## 利用模块实现单例模式

单例是最常使用的模式，通过单例模式可以保证系统中一个类只有一个实例，而且该实例易于被外界访问，从而方便对实例个数的控制并节约系统资源。比如要实现一个xxxManage的类时，往往意味着这是一个单例。

以下方法基本可以保证“只能有一个实例”：

```python
class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

if __name__ == '__main__':
    # s1 = Singleton()
    # s2 = Singleton()
    # print(id(s1) == id(s2))
```

上例在并发情况下可能发生意外，为了解决这个问题，可以引入一个带锁的版本：

```python
import threading

class NewSingleton(object):
    objs = {}
    objs_locker = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls in cls.objs:
            print(f"--3--, {cls.objs}")
            return cls.objs[cls]
        print(f"--1--, {cls.objs}")
        cls.objs_locker.acquire()
        try:
            if cls not in cls.objs:
                cls.objs[cls] = object.__new__(cls)
            return cls.objs[cls]
        finally:
            print(f"--2--, {cls.objs}")
            cls.objs_locker.release()

if __name__ == '__main__':
    s1 = NewSingleton()
    s2 = NewSingleton()
    print(id(s1) == id(s2))
    # --1--, {}
    # --2--, {<class '__main__.NewSingleton'>: <__main__.NewSingleton object at 0x000001E50B42A5C0>}
    # --3--, {<class '__main__.NewSingleton'>: <__main__.NewSingleton object at 0x000001E50B42A5C0>}
```

利用经典的双检查锁机制，确保了再并发环境下单例的正确实现。

但是依然存在一些问题：

- 如果NewSingleton的子类重载了`__new__()`方法，会覆盖或者干扰NewSingleton类中`__new__()`的执行，虽然概率较小，但是不可忽视；
- 若子类中有`__init__()`方法，那么每次实例化该Singleton时，`__init__()`方法都会被调用到，这显然是不应该的，`__init__()`只应该在创建实例的时候被调用一次。

其实，Python中的模块采用的是天然的单例的实现方式：

- 所有的变量都会绑定到模块
- 模块只初始化一次
- import 机制是线程安全的（保证了再并发状态下模块也只有一个实例）

因此，想要实现一个单例，只需要简单的创建一个py文件即可。

