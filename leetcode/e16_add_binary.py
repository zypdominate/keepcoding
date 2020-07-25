# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:二进制求和
@time:2020/5/8 20:13
"""
'''
给你两个二进制字符串，返回它们的和（用二进制表示）。
输入为 非空 字符串且只包含数字 1 和 0。

示例 1:
输入: a = "11", b = "1"
输出: "100"

示例 2:
输入: a = "1010", b = "1011"
输出: "10101"

提示：
每个字符串仅由字符 '0' 或 '1' 组成。
1 <= a.length, b.length <= 10^4
字符串如果不是 "0" ，就都不含前导零。
'''


class Solution:
    def compare(self, result, cur, plus):
        '''
        计算对应位上的结果
        :param result: 拼接的字符串
        :param cur: 当前位的值 0 或 1
        :param plus: 进位数，进位1 不进位0
        '''
        if cur + plus == 3:  # 每位计算结果无非3种结果
            plus = 1
            result += '1'
        elif cur + plus == 2:
            plus = 1
            result += '0'
        elif cur + plus == 1:
            plus = 0
            result += '1'
        else:
            plus = 0
            result += '0'
        return result, cur, plus

    # 我是采用逐位计算的
    def addBinary(self, a: str, b: str) -> str:
        len_a, len_b = len(a), len(b)
        if len_a > len_b:
            longer_str = a
            len_min = len_b
            a = longer_str[::-1][0:len_min][::-1]  # 在末尾提取长字符串中，与短字符串长度相等的部分
        elif len_a < len_b:
            longer_str = b
            len_min = len_a
            b = longer_str[::-1][0:len_min][::-1]
        else:
            longer_str = None
            len_min = len_a
        plus = 0
        result = ''
        for i in range(len_min - 1, -1, -1):  # step1.计算尾部相同长度的部分
            cur = int(a[i]) + int(b[i])
            result, cur, plus = self.compare(result, cur, plus)
        if longer_str:  # step2.单独处理更长字符串的多余部分
            for i in range(len(longer_str) - len_min - 1, -1, -1):
                cur = int(longer_str[i])
                result, cur, plus = self.compare(result, cur, plus)
        if plus:
            result += str(plus)
        print(result[::-1])
        return result[::-1]

    # 看到leetcode提供的方法中有一个`a.zfill(n)`方法，顿时觉得自己还分类讨论，太low了
    def addBinary_upgrade(self, a: str, b: str) -> str:
        lenth = max(len(a), len(b))
        a, b = a.zfill(lenth), b.zfill(lenth)
        plus = 0
        result = ''
        for i in range(lenth - 1, -1, -1):  # 将a&b的长度统一，直接计算
            cur = int(a[i]) + int(b[i])
            result, cur, plus = self.compare(result, cur, plus)
        if plus:
            result += str(plus)
        return result[::-1]


if __name__ == '__main__':
    s = Solution()
    assert s.addBinary("11", "111") == s.addBinary_upgrade("11", "111")
    assert s.addBinary("1", "0") == s.addBinary_upgrade("1", "0")
    assert s.addBinary("1", "1") == s.addBinary_upgrade("1", "1")
    assert s.addBinary("11", "10") == s.addBinary_upgrade("11", "10")
    assert s.addBinary("1011", "1010") == s.addBinary_upgrade("1011", "1010")
