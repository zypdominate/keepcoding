import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FranchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamends clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit)
                       for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

f = FranchDeck()
for i in f:
    print(i)
print(len(f))
print(f[0])