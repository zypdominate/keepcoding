class A:
    def ping(self):
        print("A ping", self)

class B(A):
    def pong(self):
        print("B pong", self)

class C(A):
    def pong(self):
        print("C pong", self)

class D(B, C):
    def ping(self):
        super().ping()
        # A.ping(self)
        print("D ping", self)

    def pingpong(self):
        self.ping()  # A ping、D ping、
        super().ping()  # A ping
        self.pong()  # B pong
        super().pong()  # B pong
        C.pong(self)  # C pong

d = D()
# d.pong()  # B pong <__main__.D object at 0x000001984DC16AC8>
# C.pong(d) # C pong <__main__.D object at 0x000001984DC16AC8>
# B.pong(d) # B pong <__main__.D object at 0x000001984DC16AC8>

# print(D.__mro__)
# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)

# d.ping()
# A ping <__main__.D object at 0x0000026DB0765B38>
# D ping <__main__.D object at 0x0000026DB0765B38>

d.pingpong()
# A ping <__main__.D object at 0x0000029B132A5B38>
# D ping <__main__.D object at 0x0000029B132A5B38>
# A ping <__main__.D object at 0x0000029B132A5B38>
# B pong <__main__.D object at 0x0000029B132A5B38>
# B pong <__main__.D object at 0x0000029B132A5B38>
# C pong <__main__.D object at 0x0000029B132A5B38>
