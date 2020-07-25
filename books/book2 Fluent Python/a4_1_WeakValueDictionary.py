import weakref


class Cheese():
    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return f'Chess-{self.kind}'


stock = weakref.WeakValueDictionary()
catalog = [Cheese('Leicester'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Parmesan')]

for cheese in catalog:
    stock[cheese.kind] = cheese

del catalog
print(sorted(stock.keys()))   # ['Parmesan']

del cheese
print(sorted(stock.keys()))   # []


