import a6_2_QuantityLineItem2 as model


# 描述符的常规用法: 将描述符从另一个模块中导入
class LineItem():
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    item = LineItem('test', 10, 20)
    print(LineItem.weight)
    print(f'weight:{item.weight}, price:{item.price}')
    print(getattr(item, '_Quantity#0'), getattr(item, '_Quantity#1'))
    '''
    _Quantity#0
    _Quantity#1
    weight:10, price:20
    10 20
    '''
