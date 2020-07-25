# 1、参数传值
def test_invarible(var):
    print(var, id(var))
    var += 1
    print(var, id(var))


var = 1
print(var, id(var))
test_invarible(var)
print(var, id(var))


# 1 1380754528
# 1 1380754528
# 2 1380754560
# 1 1380754528
# 如果是引用，函数中var的id应该是不变的，且最后的var打印应该为2。


# 2、参数引用
def test_varibale(varlist):
    print(varlist, id(varlist))
    varlist.append("func")
    print(varlist, id(varlist))


originlist = [1, 2, 3]
test_varibale(originlist)
print(originlist, id(originlist))


# [1, 2, 3] 1486999385800
# [1, 2, 3, 'func'] 1486999385800
# [1, 2, 3, 'func'] 1486999385800
# 如果是传值，且最后的originlist打印应该为最初的[1, 2, 3]。


# 3、Python中的赋值原理
def function_param(origin_list):
    new_list = origin_list
    print(origin_list, id(origin_list))
    print(new_list, id(new_list))
    # new_list = [0, 0, 0]  # case1：给new_list重新分配内存地址，id改变
    new_list.append('a')  # case2：在new_list对象上更改，内存地址不变，id不变
    print(new_list, id(new_list))


origin_list = [1, 2, 3]
function_param(origin_list)
print(origin_list, id(origin_list))

'''
new_list = [0, 0, 0]时
[1, 2, 3] 1990045687496
[1, 2, 3] 1990045687496
[0, 0, 0] 1990045619720
[1, 2, 3] 1990045687496
'''
'''
new_list.append('a')时
[1, 2, 3] 2733052026568
[1, 2, 3] 2733052026568
[1, 2, 3, 'a'] 2733052026568
[1, 2, 3, 'a'] 2733052026568
'''
