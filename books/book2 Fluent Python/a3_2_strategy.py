from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem(object):
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order(object):
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = f'<Order total:{self.total()}, due:{self.due()}>'
        return fmt


class Promotion(ABC):
    @staticmethod
    def discount(self, order):
        """返回折扣金额"""


class FidelityPromo(Promotion):
    """1000积分以上顾客，5%折扣"""

    def discount(self, order):
        return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):
    """单个商品20个以上，10%折扣"""

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * 0.1
        return discount


class LargeOrderPromo(Promotion):
    """不同商品10个以上，7%折扣"""

    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * 0.07
        return 0

joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('banana', 4, .5), LineItem('apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]
Order(joe, cart, FidelityPromo())
 # <Order total: 42.00 due: 42.00>
Order(ann, cart, FidelityPromo())
 # <Order total: 42.00 due: 39.90>
banana_cart = [LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]
Order(joe, banana_cart, BulkItemPromo())
 # <Order total: 30.00 due: 28.50>
long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
Order(joe, long_order, LargeOrderPromo())
 # <Order total: 10.00 due: 9.30>
Order(joe, cart, LargeOrderPromo())