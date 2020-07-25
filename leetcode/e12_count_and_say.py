# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:外观数列
@time:2020/4/6 16:29
"""
'''
「外观数列」是一个整数序列，从数字 1 开始，序列中的每一项都是对前一项的描述。前五项如下：
1.     1
2.     11
3.     21
4.     1211
5.     111221
1 被读作  "one 1"  ("一个一") , 即 11。
11 被读作 "two 1s" ("两个一"）, 即 21。
21 被读作 "one 2",  "one 1" （"一个二" ,  "一个一") , 即 1211。

给定一个正整数 n（1 ≤ n ≤ 30），输出外观数列的第 n 项。
注意：整数序列中的每一项将表示为一个字符串。
'''
"""
示例 1:
输入: 1
输出: "1"
解释：这是一个基本样例。

示例 2:
输入: 4
输出: "1211"
解释：当 n = 3 时，序列是 "21"，其中我们有 "2" 和 "1" 两组，"2" 可以读作 "12"，也就是出现频次 = 1 而 值 = 2；类似 "1" 可以读作 "11"。所以答案是 "12" 和 "11" 组合在一起，也就是 "1211"。
"""


class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return '1'
        pre = self.countAndSay(n - 1)
        res = ''
        counter = 1
        for i in range(len(pre)):
            # 预先处理最后一个字符，避免下标越界：只需处理最后两个不同的情况
            if i == len(pre) - 1:
                res += f'1{pre[-1]}'
            else:
                if (i + 1 == len(pre) - 1) and pre[i] == pre[i + 1]:
                    # 判断倒数第二个是否等于最后一个，如果相等，返回；若不等，留给前面的预先处理来保证
                    counter += 1
                    return res + f'{counter}{pre[i]}'
                elif pre[i] == pre[i + 1]:
                    counter += 1
                else:
                    # 下一个字符与当前不同，所以要统计当前相同的字符数，并将counter清零
                    res += f'{counter}{pre[i]}'
                    counter = 1
        return res

    # 看到一种比较好的方法，不用递归：只记录前后两组
    def countAndSay2(self, n: int) -> str:
        pre = '1'
        for i in range(1, n):
            res = ''
            cmp = pre[0]
            count = 1
            for j in range(1, len(pre)):
                if pre[j] == cmp:
                    count += 1
                else:
                    res += str(count) + cmp
                    cmp = pre[j]
                    count = 1
            res += str(count) + cmp
            pre = res
        return pre


if __name__ == '__main__':
    s = Solution()
    print([s.countAndSay(n) for n in range(1, 7)])
    print([s.countAndSay2(n) for n in range(1, 7)])
    # 11 21 1211 111221  312211
