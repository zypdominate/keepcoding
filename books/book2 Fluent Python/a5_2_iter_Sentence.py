import re
import reprlib

RE_WORD = re.compile("\w+")


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError as e:
            raise StopIteration
        self.index += 1
        return word

    def __iter__(self):
        return self


class Sentence:
    def __init__(self, text):
        self.text = text
        self.word = RE_WORD.findall(text)

    def __repr__(self):
        return f"{type(self).__name__}:{reprlib.repr(self.text)}"

    def __iter__(self):  # 明确表明这个类可以迭代
        # 根据可迭代协议，__iter__ 方法实例化并返回一个迭代器。
        return SentenceIterator(self.word)


# 在SentenceIterator中实现 __iter__ 可以让能让迭代器通过以下测试：
from collections import abc
print(issubclass(SentenceIterator, abc.Iterator))

s = Sentence("a b c")
for i in s:
    print(i)