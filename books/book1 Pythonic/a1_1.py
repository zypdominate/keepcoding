# 快排

def quickSort(array):
    less, more = [], []
    if len(array) <= 1:
        return array
    middle = array.pop()
    for i in array:
        if i < middle:
            less.append(i)
        else:
            more.append(i)
    return quickSort(less) + [middle] + quickSort(more)

testArray = [2,1,6,3,9,8]
print(quickSort(testArray))

