# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:
@time:2020/3/24 18:09
"""
'''
最长公共前缀:
编写一个函数来查找字符串数组中的最长公共前缀。
如果不存在公共前缀，返回空字符串 ""。
'''
"""
示例 1:
输入: ["flower","flow","flight"]
输出: "fl"

示例 2:
输入: ["dog","racecar","car"]
输出: ""
解释: 输入不存在公共前缀。

说明:
所有输入只包含小写字母 a-z 。
"""
from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        min_len = min([len(s) for s in strs])
        i, issame, str_same = 0, True, ''
        while i < min_len:
            cmp = strs[0][i]
            for s in strs[1:]:  # 将第一个字符串中的每个字符，与列表中的其余字符串的同位置比较
                if cmp == s[i]:
                    continue
                else:
                    issame = False
                    break
            if issame:
                str_same += cmp
            else:
                break  # 只要有一个不同，跳出while循环，后面的就不用比较了
            i += 1

        return str_same

    # 学到一种利用 zip 的方法，很巧妙
    def longestCommonPrefix2(self, strs: List[str]) -> str:
        s = ''
        for i in zip(*strs):
            if len(set(i)) == 1:
                s += i[0]
            else:
                break
        return s


if __name__ == '__main__':
    s = Solution()
    print(s.longestCommonPrefix(["flower", "flower", "fliger"]))
    print(s.longestCommonPrefix(["dog", "racecar", "car"]))

"""
补充点：
l = ["flower", "flower", "fliger"]

zip(*l)
Out[3]: <zip at 0x2139bb82088>

list(zip(*l))
Out[4]: 
[('f', 'f', 'f'),
 ('l', 'l', 'l'),
 ('o', 'o', 'i'),
 ('w', 'w', 'g'),
 ('e', 'e', 'e'),
 ('r', 'r', 'r')]

"""
