# 工厂函数
def quantity(storage_name):
    def qty_getter(instance):
        # 值直接从 instance.__dict__ 中获取，为的是跳过特性，防止无限递归。
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value  # 也是为了跳过特性
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    weight = quantity('weight')
    price = quantity('price')

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
