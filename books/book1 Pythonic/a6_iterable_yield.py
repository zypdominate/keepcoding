
def traditional(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield b
        a, b = b, a + b
        count += 1

# print(list(traditional(5)))
# print(dir(traditional(5)))


def echo(value):
    print("**begin")
    while True:
        try:
            value = yield value
        except Exception as e:
            print(e)
        finally:
            print("finish**")

gen = echo(1)
# print(gen.__next__())
# print(gen.__next__())
print(next(gen))
print(next(gen))
print(gen.send(2))
# print(gen.__next__())

