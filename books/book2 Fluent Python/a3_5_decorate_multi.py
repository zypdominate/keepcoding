
def d1(func):
    def decorate1(*args,**kwargs):
        print(f'd1 decorate')
    return decorate1

def d2(func):
    def decorate2(*args,**kwargs):
        print(f'd2 decorate')
    return decorate2

@d1
@d2
def f():
    print('f')

f()


# 等同于：
# def f():
#     print('f')
# f = d1(d2(f))