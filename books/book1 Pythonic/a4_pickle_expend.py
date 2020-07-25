import pickle


class TextReader():
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename)  # 打开文件的句柄
        self.position = self.file.tell()

    def readline(self):
        line = self.file.readline()
        self.position = self.file.tell()
        if not line:
            return None
        if line.endswith('\n'):
            line = line[:-1]
        return f"{self.position}", line

    def __getstate__(self):  # 记录文件被pickle时的状态
        print("in __getstate__")
        state = self.__dict__.copy()  # 获取被pickle时的字典信息
        del state['file']
        return state

    def __setstate__(self, state):  # 设置反序列化后的状态
        print("in __setstate__")
        self.__dict__.update(state)
        file = open(self.filename)
        self.file = file


reader = TextReader("test.py")
print(reader.readline())
print(reader.readline())
print("---")

s = pickle.dumps(reader)  # 在dumps时会默认调用__getstate__
new_reader = pickle.loads(s)  # 在loads时会默认调用__setstate__
print("***")
print(new_reader.readline())
print(new_reader.readline())
