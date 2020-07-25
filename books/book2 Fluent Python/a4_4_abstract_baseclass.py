import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()  # 黑桃 方块 梅花 红心

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    # 为了支持洗牌，只需要实现__setitem__方法
    def __setitem__(self, position, value):
        self._cards[position] = value

    # 继承MutableSequence类，必须实现它的一个抽象方法__delitem__
    def __delitem__(self, position):
        del self._cards[position]

    # 还要实现 insert 方法，这是 MutableSequence 类的第三个抽象方法。
    def insert(self, position, value):
        self._cards.insert(position, value)

french = FrenchDeck2()
