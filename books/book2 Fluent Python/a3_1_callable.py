import random


class BingoCase(object):
    def __init__(self, items):
        self._items = list(items)  # 接受任何可迭代对象，在本地构建一个副本，防止列表参数的意外副作用
        random.shuffle(self._items)

    def pickitem(self):
        try:
            return self._items.pop()
        except IndexError as e:
            raise LookupError('pick from empty BingoCase')

    def __call__(self, *args, **kwargs):  # bingo.pickitem()的快捷方式为bingo()
        return self.pickitem()


bingo = BingoCase([1, 2, 3, 3, 4, 5])
print(bingo.pickitem())
print(bingo())
print(callable(bingo))
