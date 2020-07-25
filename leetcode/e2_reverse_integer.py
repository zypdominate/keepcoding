'''
整数反转：
给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−2**31,  2**31 − 1]。
请根据这个假设，如果反转后整数溢出那么就返回 0。
'''
"""
输入: 123
输出: 321

输入: -123
输出: -321

输入: 120
输出: 21
"""


class Solution:
    def reverse(self, x: int) -> int:
        str_x = str(x)
        if not str_x.startswith('-'):
            res = int(str_x[::-1])
        else:
            res = int(str_x[:0:-1])
            res = - res
        return res if -2147483648 < res < 2147483647 else 0


if __name__ == '__main__':
    s = Solution()
    print(s.reverse(-9))
