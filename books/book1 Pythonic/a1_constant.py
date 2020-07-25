
class Constant(object):
    class ConstError(TypeError):pass
    class ConstCaseError(ConstError):pass
    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError(f"Cant't change constant {key}")
        if not key.isupper():
            raise self.ConstCaseError(f"constant {key} is not all uppercase")
        self.__dict__[key] = value

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return None


import sys
# sys.modules[__name__]: <module '__main__'>
sys.modules[__name__] = Constant
# sys.modules[__name__]: __main__._constant

if __name__ == '__main__':

    for item in sys.modules:
        print(sys.modules[item])  # 存在<class '__main__._constant'>

    print(sys.modules[__name__])  # <class '__main__._constant'>

    Constant.NAME = 'test_const'
    print(Constant.NAME)







