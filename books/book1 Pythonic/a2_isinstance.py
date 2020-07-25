class UserInt(int):  # 继承int
    def __init__(self, var=0):
        # self._var = int(var)
        super(UserInt, self).__init__()
        self._var = int(var)

    def __add__(self, other):
        if isinstance(other, UserInt):
            return UserInt(self._var + other._var)
        return self._var + other

    def __iadd__(self, other):
        raise NotImplementedError("not support operation")

    def __str__(self):
        return str(self._var)

    def __repr__(self):
        return f"Interger {self._var}"


user1 = UserInt()
user2 = UserInt(2)
user3 = UserInt('3')
print(user1, user2, user3)  # 0 2 3
print(user1 + user2)  # 2
print(user3 + 12)  # 15

type_user1 = type(user1)  # <class '__main__.UserInt'>
type_int = type(int)  # <class 'type'>

print(type_user1 == type_int)  # False


# 使用isinstance：
isinstance(user1, type(UserInt()))  # True
isinstance(user1, int)  # True


# 比较：
print(UserInt, type(UserInt))  # <class '__main__.UserInt'> <class 'type'>
print(isinstance(UserInt,type(UserInt))) # True

print(UserInt(), type(UserInt()))  # 0 <class '__main__.UserInt'>
print(isinstance(UserInt(),type(UserInt()))) # True

print(user1, type(user1))  # 0 <class '__main__.UserInt'>
print(isinstance(user1,type(user1)))

print(int, type(int))  # <class 'int'> <class 'type'>
print(isinstance(int,type(int)))  # True
print(isinstance(1, int))  # True
