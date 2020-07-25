def gen():
    for i in "ABC":
        yield i
    for j in [1, 2, 3]:
        yield j


print(list(gen()))  # ['A', 'B', 'C', 1, 2, 3]


def gen2():
    yield from "ABC"
    yield from [1, 2, 3]


print(list(gen2()))


def gen3(*args):
    for item in args:
        yield from item


a = (1, 2, 3)
b = "ABC"
print(list(gen3(a, b)))  # [1, 2, 3, 'A', 'B', 'C']
