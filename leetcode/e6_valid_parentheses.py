# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:有效的括号
@time:2020/3/25
"""
'''
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。

有效字符串需满足：
左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。
注意空字符串可被认为是有效字符串。
'''
"""
示例 1:

输入: "()"
输出: true
示例 2:

输入: "()[]{}"
输出: true
示例 3:

输入: "(]"
输出: false
示例 4:

输入: "([)]"
输出: false
示例 5:

输入: "{[]}"
输出: true
"""


class Solution:
    def isValid(self, s: str) -> bool:
        dicts = {'(': ')', ')': '(', '[': ']', ']': '[', '{': '}', '}': '{'}
        lists = list(s)
        lens = len(s)
        if lens == 2 and lists[0] != dicts.get(lists[1]):
            return False
        if len(s) % 2 == 1:
            return False
        i = 0
        while len(lists):
            if lists[i] == dicts.get(lists[i + 1]):
                lists.pop(i + 1)
                lists.pop(i)
                i = 0
            else:
                i += 1
                if i == (len(lists) - 2):
                    return False
                elif len(lists) == 2 and lists[0] != dicts.get(lists[1]):
                    return False
                else:
                    continue
        return True


# 学习：栈先入后出
class Solution2:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 == 1:
            return False
        dic = {'{': '}', '[': ']', '(': ')', '?': '?'}
        stack = ['?']
        for c in s:
            if c in dic:
                stack.append(c)
            elif dic[stack.pop()] != c:
                return False
        return len(stack) == 1


class Solution_upgrade:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 == 1:  # 长度为奇数的s直接判断
            return False
        dic = {'{': '}', '[': ']', '(': ')'}
        stack = []
        for c in s:
            if c in dic:
                stack.append(c)
            elif len(stack) == 0:  # 以左括号开口的s，第一个字符不会append到stack，这时len(stacl)为0
                return False
            elif dic[stack.pop()] != c:
                return False
        return len(stack) == 0


if __name__ == '__main__':
    # s = Solution()
    s = Solution2()
    print([s.isValid(i) for i in ["){", "((", "{(())}[()]", "{[]}", "()", "()[]{}", "([]){}", "()[]{}", "()",
                                  "(()(", "(]", "([)]", "([)"]])
