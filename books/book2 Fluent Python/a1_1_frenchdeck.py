import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()  # 黑桃 方块 梅花 红心

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


deck = FrenchDeck()
print(len(deck))  # len()的使用是使用 __len__ 函数
print(deck[0])   # 抽取特定序号的元素，如最后一个deck[-1]，由__getitem__提供


from random import choice
choice(deck)
# Out[5]: CardName(rank='8', suit='clubs')
choice(deck)
# Out[6]: CardName(rank='K', suit='hearts')


# 由于__getitem__方法把列表[]操作交给了self._cards列表，所以deck类自动支持切片操作
print(deck[:3])
print(deck[12::13]) # 取索引为12的牌，再每隔13张取一次


# 可迭代
for item in deck:
    print(item)
# 反向迭代
for item in deck:
    print(item)


# in 运算符
Card(rank='2', suit='spades') in deck
# Out[7]: True
Card(rank='2', suit='opades') in deck
# Out[8]: False


# 排序：先看点数，再比较花色
# 点数：2最小，A最大； 花色：黑桃>红桃>方块>梅花  --> 梅花2最小，为0，黑桃A最大，为52
suit_values =dict(spades=3, hearts=2, diamonds=1, clubs=0)
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)   # 考虑到有字母，比较大小用下标
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(deck,key=spades_high):
    print(card)