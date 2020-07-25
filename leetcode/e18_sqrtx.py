# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:实现 int sqrt(int x) 函数。
@time:2020/6/4 12:36
"""
'''
计算并返回 x 的平方根，其中 x 是非负整数。
由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。

示例 1:
输入: 4
输出: 2

示例 2:
输入: 8
输出: 2
说明: 8 的平方根是 2.82842..., 
     由于返回类型是整数，小数部分将被舍去。
'''
"""
For a natural number x (i.e. x ∈ {0,1,2,3,...}), 
the integer square root of x is defined as the natural number r such that r2 ≤ x < (r + 1)2. 
It is the greatest r such that r2 ≤ x, or equivalently, the least r such that (r + 1)2 > x. 
"""


class Solution:
    def average(self, x, y):
        return (x + y) / 2

    def mySqrt(self, x: int) -> int:
        smaller, bigger = 1, x
        middle = self.average(smaller, bigger)
        while True:
            if middle ** 2 > x:
                bigger = middle
                middle = self.average(smaller, middle)
            else:
                smaller = middle
                middle = self.average(middle, bigger)
            if x <= middle ** 2 < x + 1:
                break
        return middle // 1

    # 递归法：只作为一种方法，在leetcode上提交会超时
    def mySqrt2(self, x):
        '''
        方法来源：http://www.nuprl.org/MathLibrary/integer_sqrt/
        '''
        if x == 0:
            return 0
        else:
            r2 = self.mySqrt2(x - 1)
            r3 = r2 + 1
            if x < r3 ** 2:
                return r2
            else:
                return r3


if __name__ == '__main__':
    s = Solution()
    assert s.mySqrt(1) == 1
    assert s.mySqrt(4) == 2
    assert s.mySqrt(8) == 2
    assert s.mySqrt(9) == 3
