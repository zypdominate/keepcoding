
# 不推荐在finally中使用return语句进行返回，
# 这种处理方式不仅会带来误解，可能还会导致严重的错误。

def test_finally(n):
    try:
        if n <= 0:
            raise ValueError('data is negative')
        else:
            return n
    except ValueError as e:
        print(e)
    finally:
        return -1


print(test_finally(0))  # -1
print(test_finally(2))  # -1 其实是想得到2的
