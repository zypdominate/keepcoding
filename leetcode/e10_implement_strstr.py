# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:
@time:2020/4/1 18:34
"""
'''
实现 strStr() 函数。
给定一个 haystack 字符串和一个 needle 字符串，
在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。
如果不存在，则返回  -1。
'''
"""
示例 1:
输入: haystack = "hello", needle = "ll"
输出: 2

示例 2:
输入: haystack = "aaaaa", needle = "bba"
输出: -1
说明:
当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。
对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与C语言的 strstr() 以及 Java的 indexOf() 定义相符。
"""


class Solution:
    # 将 needle 沿着 haystack 滑动，逐一比较子串，时间复杂度为O((N-L)L)
    def strStr(self, haystack: str, needle: str) -> int:
        # if len(needle) == 0: return 0
        index = 0
        len_haystack, len_needle = len(haystack), len(needle)
        while index <= len_haystack - len_needle:
            if haystack[index:index + len_needle] == needle:
                return index
            index += 1
        return -1

    # 内置的 find 方法，这个方法可以，但是我没有第一时间想到，但是这样做就没意思了。
    def strStr1(self, haystack: str, needle: str) -> int:
        return haystack.find(needle)


if __name__ == '__main__':
    s = Solution()
    assert s.strStr(haystack="hello", needle="") == 0
    assert s.strStr(haystack="hello", needle="ll") == 2
    assert s.strStr(haystack="aaaaa", needle="bba") == -1
    assert s.strStr(haystack="aaabbaa", needle="bba") == 3
