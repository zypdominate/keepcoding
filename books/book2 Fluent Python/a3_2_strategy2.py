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
            discount = self.promotion(self)  # 计算折扣只需调用self.promotion()函数。
        return self.total() - discount

    def __repr__(self):
        fmt = f'<Order total:{self.total()}, due:{self.due()}>'
        return fmt


# 没有抽象类
def fidelity_promo(order):  # 各个策略都是函数
    """1000积分以上顾客，5%折扣"""
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    """单个商品20个以上，10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * 0.1
    return discount


def large_order_promo(order):
    """不同商品10个以上，7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.07
    return 0


joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('banana', 4, .5), LineItem('apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]

Order(joe, cart, fidelity_promo)
# <Order total: 42.00 due: 42.00>
Order(ann, cart, fidelity_promo)
# <Order total: 42.00 due: 39.90>

banana_cart = [LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]
Order(joe, banana_cart, bulk_item_promo)
# <Order total: 30.00 due: 28.50>
long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
Order(joe, long_order, large_order_promo)
# <Order total: 10.00 due: 9.30>
Order(joe, cart, large_order_promo)
# <Order total:42.0, due:42.0>


# 选择最佳策略：方法一
promo_list = [fidelity_promo, bulk_item_promo, large_order_promo]
def best_promo(order):
    """
    与其他几个 *_promo 函数一样，best_promo 函数的参数是一个Order实例;
    使用生成器表达式把 order 传给 promos 列表中的各个函数，
    返回折扣额度最大的那个函数。
    """
    return max(promo(order) for promo in promo_list)


# 选择最佳策略：方法二
promo_list2 = [globals()[name] for name in globals()
          if name.endswith('_promo') and name != 'best_promo']
def best_promo2(order):
    # 选择可用的最佳折扣
    return max(promo(order) for promo in promo_list2)


print(Order(joe, banana_cart, bulk_item_promo))
print(Order(joe, long_order, large_order_promo))
print(Order(joe, cart, best_promo2))
# <Order total:30.0, due:28.5>
# <Order total:10.0, due:9.3>
# <Order total:42.0, due:42.0>