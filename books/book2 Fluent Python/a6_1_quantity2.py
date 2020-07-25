# 使用特性工厂函数实现，与描述符类相同的功能
def quantity():  # 没有storage_name参数
    try:
        # 不能依靠类属性在多次调用之间共享counter，因此把它定义为quantity函数自身的属性。
        quantity.counter += 1
    except AttributeError:
        quantity.counter = 0
    # 也没有实例变量，因此创建一个局部变量storage_name，借助闭包保持它的值，供后面的qty_getter和qty_setter函数使用。
    storage_name = f'_quantity_{quantity.counter}'
    print(storage_name)

    # 这里可以使用内置的getattr和setattr函数，而不用处理instance.__dict__属性。
    def qty_getter(instance):
        # 值直接从 instance.__dict__ 中获取，为的是跳过特性，防止无限递归。
        # return instance.__dict__[storage_name]
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            # instance.__dict__[storage_name] = value  # 也是为了跳过特性
            setattr(instance, storage_name, value)
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    weight = quantity()
    price = quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    item = LineItem("Test Item", 8, 18)
    print(item.weight, item.price)
    print(sorted(vars(item).items()))
    '''
    _quantity_0
    _quantity_1
    8 18
    [('_quantity_0', 8), ('_quantity_1', 18), ('description', 'Test Item')]
    '''
