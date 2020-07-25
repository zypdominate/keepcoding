# 统计次数
# 1、使用dict
data = ['a', '2', 'c', 1, 2, 'a', 'c', 'a', 'b', 0, 1]
count_dict = dict()
for ele in data:
    if ele in count_dict:
        count_dict[ele] +=1
    else:
        count_dict[ele] = 1
# count_dict
# Out[1]: {'a': 3, '2': 1, 'c': 2, 1: 2, 2: 1, 'b': 1, 0: 1}


# 2、使用defaultdict
from collections import defaultdict
count_default = defaultdict(int)
for ele in data:
    count_default[ele] +=1
# count_default
# Out[2]: defaultdict(int, {'a': 3, '2': 1, 'c': 2, 1: 2, 2: 1, 'b': 1, 0: 1})


# 3、使用set和list
count_set = set(data)
count_list = []
for ele in count_set:
    count_list.append((ele, data.count(ele)))
# count_list
# Out[3]: [(0, 1), (1, 2), ('2', 1), (2, 1), ('c', 2), ('b', 1), ('a', 3)]


# 4、更加优雅、简介的方式：使用collection.Counter
# Counter类属于字典类的子类，是一个容器对象，主要用来统计散列对象
# 支持集合操作+-&|，其中&|分别返回两个Counter对象元素的最小值和最大值
from collections import Counter
# 三种方式初始化：可迭代对象、关键字参数、字典
Counter('success')      # Counter({'s': 3, 'u': 1, 'c': 2, 'e': 1})
Counter(a=1, b=2, c=3)      # Counter({'a': 1, 'b': 2, 'c': 3})
Counter({'a': '2', 'c': 1, 2: 'a'})  # Out[8]: Counter({'a': '2', 'c': 1, 2: 'a'})



# 使用element()方法来获取Counter中的key值
data = ['a', '2', 'c', 1, 2, 'a', 'c', 'a', 'b', 0, 1]
list(Counter(data).elements())
# Out[10]: ['a', 'a', 'a', '2', 'c', 'c', 1, 1, 2, 'b', 0]

# 使用most_common()方法找出前n个出现频率最高的元素、对应次数
Counter(data).most_common(2)
# Out[12]: [('a', 3), ('c', 2)]

# 当访问的元素不存在时，默认返回0，而不是抛出异常
(Counter(data)['y'])
# Out[13]: 0

# updata()方法用于被统计对象元素的更新，原有Counter计数器对象和新增元素的统计数值相加而不是直接替换它们
c = Counter('success')
# c
# Out[15]: Counter({'s': 3, 'u': 1, 'c': 2, 'e': 1})
c.update('successfully')
# c
# Out[17]: Counter({'s': 6, 'u': 3, 'c': 4, 'e': 2, 'f': 1, 'l': 2, 'y': 1})

# subtract()用于实现计数器对象中元素统计值相减，输入和输出的统计值允许为0或者为负数
c.subtract('successfully')
# c
# Out[19]: Counter({'s': 3, 'u': 1, 'c': 2, 'e': 1, 'f': 0, 'l': 0, 'y': 0})
