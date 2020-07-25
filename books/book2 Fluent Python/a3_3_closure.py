# 使用class
class Avg(object):
    def __init__(self):
        self.series = []

    def __call__(self, newvalue):
        self.series.append(newvalue)
        return sum(self.series) / len(self.series)


avg = Avg()
print(avg(1))
print(avg(3))


# 使用函数
def average():
    series = []
    def avg(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)
    return avg


avg2 = average()
print(avg2.__closure__[0].cell_contents) # []
print(avg2(3))  # 3.0
print(avg2(9))  # 6.0

print(avg2.__code__.co_varnames)  # ('new_value', 'total')
print(avg2.__code__.co_freevars)  # ('series',)
print(avg2.__closure__[0].cell_contents)  # [3, 9]
