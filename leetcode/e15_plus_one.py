# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:
@time:2020/5/5 22:57
"""
'''
给定一个由整数组成的非空数组所表示的非负整数，在该数的基础上加一。
最高位数字存放在数组的首位， 数组中每个元素只存储单个数字。
你可以假设除了整数 0 之外，这个整数不会以零开头。

示例 1:
输入: [1,2,3]
输出: [1,2,4]
解释: 输入数组表示数字 123。

示例 2:
输入: [4,3,2,1]
输出: [4,3,2,2]
解释: 输入数组表示数字 4321。
'''
from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        addone = True  # 每一位是否需要进位的标志
        len_digits = len(digits)
        for i in range(len_digits - 1, -1, -1):  # 倒序
            if addone:
                if digits[i] == 9:
                    digits[i] = 0
                else:
                    digits[i] += 1
                    addone = False
            else:
                break
            if i == 0 and addone:
                digits.insert(0, 1)
        return digits


if __name__ == '__main__':
    s = Solution()
    print(s.plusOne([1, 2, 3]))
    print(s.plusOne([4, 3, 2, 1]))
    print(s.plusOne([9]))
