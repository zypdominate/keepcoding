class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):  # 使得'Fib' object is iterable
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a


for i, j in enumerate(Fib()):
    print(j)
    if i > 10:
        break


def traditional(n):
    reslist = []
    a, b = 0, 1
    count = 0
    while count < n:
        reslist.append(b)
        a, b = b, a + b
        count += 1
    return reslist

print(traditional(10))
