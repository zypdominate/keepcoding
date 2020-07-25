
# a1_constant中添加sys.modules[__name__] = Constant后,下一行代码无法导包Constant
# from myLearning.python.book1.a1_constant import Constant
# Constant.NAME = 'test_name'
# print(Constant.NAME)

# Mark Directory Path as Source Root
from myLearning.python.book1 import a1_constant

a1_constant.NAME = 'test_name111'
print(a1_constant.NAME)


import a1_constant

a1_constant.NAME = 'test_name222'
print(a1_constant.NAME)


# import 后的对象将加入到 sys.module中
print(dir())
from a1_constant_testmodule import a  # 将 a 加入到sys.module中
# import a1_constant_testmodule  # 将 test_module 加入到sys.module中
print(dir())
