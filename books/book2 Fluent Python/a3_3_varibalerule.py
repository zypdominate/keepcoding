
b = 1
c = 3
def f1(a):
    print(a)
    print(b)
    print(c)
    b = 2

from dis import dis

dis(f1)