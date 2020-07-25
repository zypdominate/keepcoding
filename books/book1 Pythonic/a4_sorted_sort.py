from operator import itemgetter

# 1、对字典排序
bookowner = {'Bob': '2', 'Caly': '1', 'Amy': '3'}

sorted(bookowner.items(), key=itemgetter(1))
# Out[1]: [('Caly', '1'), ('Bob', '2'), ('Amy', '3')]

sorted(bookowner.items(), key=itemgetter(0))
# Out[2]: [('Amy', '3'), ('Bob', '2'), ('Caly', '1')]


# 2、多维list排序
info = [['Bob', 95, 'A'], ['Caly', 86, 'C'], ['justin', 82, 'A'], ['Amy', 86, 'D']]
sorted(info, key=itemgetter(2, 1))
# Out[2]: [['justin', 82, 'A'], ['Bob', 95, 'A'], ['Caly', 86, 'C'], ['Amy', 86, 'D']]


# 3、字典中的混合list排序
mydict = {
    'Bob': ['M', 7],
    'Caly': ['E', 2],
    'Justin': ['P', 3],
    'Amy': ['C', 6]
}
sorted(mydict.items(), key=lambda elem: itemgetter(1)(elem[1]))
# sorted(mydict.items(), key=lambda(k,v): itemgetter(1)(v)) # python2可用
# tuple parameter unpacking is not supported in Python
# 注释：在python3中不能使用 lamda (k,v):(v,k)这种小括号了。


# 4、list中混合字典排序
ratelist = [
    {'name':'Bob','win':10,'loss':3,'rate':75},
    {'name':'David','win':3,'loss':5,'rate':57},
    {'name':'Carol','win':4,'loss':5,'rate':57},
    {'name':'Patty','win':9,'loss':3,'rate':71},
]
sorted(ratelist,key=itemgetter('rate','name'))
# Out[62]:
# [{'name': 'Carol', 'win': 4, 'loss': 5, 'rate': 57},
#  {'name': 'David', 'win': 3, 'loss': 5, 'rate': 57},
#  {'name': 'Patty', 'win': 9, 'loss': 3, 'rate': 71},
#  {'name': 'Bob', 'win': 10, 'loss': 3, 'rate': 75}]