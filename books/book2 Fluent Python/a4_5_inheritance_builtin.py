from collections import UserDict


# 内置类型dict的__init__和__update__方法会忽略我们覆盖的__setitem__方法
# class DoppelDict(dict):

class DoppelDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [key] * 2)

d = DoppelDict(one=1)
d["two"] = 2
d.update(three=3)
print(d)
# {'one': 1, 'two': ['two', 'two'], 'three': 3}
# {'one': ['one', 'one'], 'two': ['two', 'two'], 'three': ['three', 'three']}



# dict.update 方法会忽略 AnswerDict.__getitem__ 方法
# class answerDict(dict):

class answerDict(UserDict):
    def __getitem__(self, item):
        return 100

ad = answerDict(one=1)
print(ad["one"])  # 100
new_ad = {}
new_ad.update(ad)
print(new_ad)  # {'one': 1}  # {'one': 100}
print(new_ad["one"])  # 1    # 100
