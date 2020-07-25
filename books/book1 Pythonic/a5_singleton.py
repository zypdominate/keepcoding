import threading


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class NewSingleton(object):
    objs = {}
    objs_locker = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls in cls.objs:
            print(f"--3--, {cls.objs}")
            return cls.objs[cls]
        print(f"--1--, {cls.objs}")
        # cls.objs_locker.acquire()
        # try:
        #     if cls not in cls.objs:
        #         cls.objs[cls] = object.__new__(cls)
        #     return cls.objs[cls]
        # finally:
        #     print(f"--2--, {cls.objs}")
        #     cls.objs_locker.release()

        # 使用with上下文管理acquire, release
        with cls.objs_locker:
            try:
                if cls not in cls.objs:
                    cls.objs[cls] = object.__new__(cls)
                return cls.objs[cls]
            except Exception as e:
                print(e)
            finally:
                print(f"--2--, {cls.objs}")


if __name__ == '__main__':
    # s1 = Singleton()
    # s2 = Singleton()
    # print(id(s1) == id(s2))

    s1 = NewSingleton()
    s2 = NewSingleton()
    print(id(s1) == id(s2))
    # --1--, {}
    # --2--, {<class '__main__.NewSingleton'>: <__main__.NewSingleton object at 0x000001E50B42A5C0>}
    # --3--, {<class '__main__.NewSingleton'>: <__main__.NewSingleton object at 0x000001E50B42A5C0>}
