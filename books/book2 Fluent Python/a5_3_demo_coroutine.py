def simple_coroutine():
    print("Coroutines started")
    var = yield
    print(f"Coroutines received {var}")

cor = simple_coroutine()
print(cor)
# next(cor)     # way1：motivate coroutine
# cor.send(None)    # way2：motivate coroutine
# cor.send(123)


from inspect import getgeneratorstate

def simple_coroutine2(a):
    print(f"——> started a:{a}")
    b = yield a
    print(f"——> receiced b:{b}")
    c = yield a + b
    print(f"——> receiced c:{c}")

cor2 = simple_coroutine2(1)
print(getgeneratorstate(cor2))  # GEN_CREATED

print(cor2.send(None))
print(getgeneratorstate(cor2))  # GEN_SUSPENDED

print(cor2.send(2))
print(cor2.send(10))





