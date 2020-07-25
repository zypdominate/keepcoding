import re
import reprlib
from collections import abc

RE_WORD = re.compile("\w+")


class Sentence:
    '''
    定义了一个 Sentence 类，通过索引从文本中提取单词。
    '''

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, item):
        return self.words[item]

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        print(reprlib.repr(self.text))
        return f"{type(self).__name__}({self.text}):{self.words}"


sentence = Sentence('"The time has come," Tom said,')
print(sentence)
for i in sentence:
    print(i, end=' ')
print("\n" + sentence[0], sentence[-1])

print(iter(sentence))  # <iterator object at 0x000001E1A53E7AC8>
print(isinstance(sentence, abc.Iterable))  # False
# s = 1
# print(iter(s))  # TypeError: 'int' object is not iterable


s1 = Sentence("I am zyp")
iter_s1 = iter(s1)  # 使用 iter(...)函数构建迭代器

print(isinstance(iter_s1, abc.Iterable))  # True
print(isinstance(iter_s1, abc.Iterator))  # True

print(next(iter_s1))  # I 使用 next(...) 函数使用迭代器
print(next(iter_s1))  # am
print(next(iter_s1))  # zyp
# print(next(iter_sentence))  # StopIteration
print(list(iter_s1))  # []

print(next(iter(s1)))  # I # 重新传入可迭代对象
print(list(iter(s1)))  # ['I', 'am', 'zyp']
