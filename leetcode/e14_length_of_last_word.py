# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description: 最后一个单词的长度
@time:2020/4/20 23:24
"""
'''
给定一个仅包含大小写字母和空格 ' ' 的字符串 s，返回其最后一个单词的长度。
如果字符串从左向右滚动显示，那么最后一个单词就是最后出现的单词。
如果不存在最后一个单词，请返回 0 。
说明：一个单词是指仅由字母组成、不包含任何空格字符的 最大子字符串。

示例:
输入: "Hello World"
输出: 5
'''


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        s_len = len(s)
        # 如果s中没有任何内容，返回0
        if s_len == 0:
            return 0
        count = 0  # 给最后一个单词的长度计数
        for i in range(s_len - 1, -1, -1):  # 从后往前校验
            # 不是空的时候，开始计数
            if s[i] != ' ':
                count += 1
            # 如果count已经在统计时，且s中当前元素的前一个是空，且不是首个元素时返回count
            if count and s[i - 1] == ' ' and i - 1 >= 0:
                return count
        # 如果s中只有一个单词，且该单词前面没有空了，返回count
        return count

    def lengthOfLastWord2(self, s: str) -> int:
        s_len = len(s)
        if s_len == 0:
            return 0
        count = 0
        # 同时利用continue和break，处理一个单词的前后空字符
        for i in range(s_len - 1, -1, -1):
            if s[i] == ' ':
                if count == 0:
                    continue
                else:
                    break
            count += 1
        return count


if __name__ == '__main__':
    s = Solution()
    print(s.lengthOfLastWord("Hello World"))
    print(s.lengthOfLastWord("Hello World "))
    print(s.lengthOfLastWord("Hello World   "))
    print(s.lengthOfLastWord("a"))
    print(s.lengthOfLastWord("a "))
    print(s.lengthOfLastWord(" "))
    print(s.lengthOfLastWord(""))
