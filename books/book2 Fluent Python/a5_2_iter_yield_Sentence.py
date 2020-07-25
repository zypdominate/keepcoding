import re
import reprlib

RE_WORD = re.compile("\w+")


class Sentence:
    def __init__(self, text):
        self.text = text
        self.word = RE_WORD.findall(text)

    def __repr__(self):
        return f"{type(self).__name__}:{reprlib.repr(self.text)}"

    def __iter__(self):
        for word in self.word:
            yield word


s = Sentence("a b c")
for i in s:
    print(i)
