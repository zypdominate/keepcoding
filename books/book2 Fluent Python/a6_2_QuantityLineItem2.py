class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f'_{prefix}#{index}'
        print(self.storage_name)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:  # 如果不是通过实例调用，返回描述符自身。
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must > 0')
