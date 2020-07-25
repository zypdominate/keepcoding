import a6_2_Quantity_refactor as model


class LineItem:
    description = model.NoneBlank()
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
    <__main__.Quantity object at 0x000002D5D1C8B9B0>
    weight:10, price:20
    10 20
    '''
