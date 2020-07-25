# 可变对象不能作为默认参数进行传递
class Studnent(object):
    def __init__(self, name, course=[]):
        self.name = name
        self.course = course

    def addcourse(self, course):
        self.course.append(course)

    def __str__(self):
        return f"{self.course}"

    def __repr__(self):
        self.__repr__ = self.__str__

# course=[]的Pycharm提示：
# This inspection detects when a mutable value as list or dictionary is detected in a default value for an argument.
# Default argument values are evaluated only once at function definition time,
# which means that modifying the default value of the argument will affect all subsequent calls of the function.

s1 = Studnent("A")
s1.addcourse("English")
print(s1)

s2 = Studnent("B")
s2.addcourse("Math")
print(s1)
print(s2)
'''
['English']
['English', 'Math']
['English', 'Math']
'''
