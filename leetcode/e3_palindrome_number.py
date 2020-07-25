'''
回文数
判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。
'''
"""
输入: 121
输出: true

输入: -121
输出: false
解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。

输入: 10
输出: false
解释: 从右向左读, 为 01 。因此它不是一个回文数。
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        # return str(x) == str(x)[::-1]
        if x < 0 or (x != 0 and x % 10 == 0):
            ret = False
        else:
            str_x = str(x)
            reversed = str_x[::-1]
            if reversed == str_x:
                ret = True
            else:
                ret = False
        return ret

    # 学习别人的方法
    # 方法一: 将int转化成str类型: 双向队列
    # 复杂度: O(n^2) [每次pop(0)都是O(n)..比较费时]
    def isPalindrome2(self, x: int) -> bool:
        lst = list(str(x))
        while len(lst) > 1:
            if lst.pop(0) != lst.pop():
                return False
        return True

    # 方法二: 将int转化成str类型: 双指针 (指针的性能一直都挺高的)
    # 复杂度: O(n)
    def isPalindrome3(self, x: int) -> bool:
        lst = list(str(x))
        L, R = 0, len(lst) - 1
        while L <= R:
            if lst[L] != lst[R]:
                return False
            L += 1
            R -= 1
        return True


class Solution2:  # 不将int转为string
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or (x != 0 and x % 10 == 0):
            ret = False
        elif x == 0:
            ret = True
        else:
            reverse_x = 0
            while x > reverse_x:
                remainder = x % 10
                reverse_x = reverse_x * 10 + remainder
                x = x // 10
            # 当x为奇数时, 只要满足 reverse_x//10 == x 即可
            if reverse_x == x or reverse_x // 10 == x:
                ret = True
            else:
                ret = False
        return ret


if __name__ == '__main__':
    s = Solution2()
    print([s.isPalindrome(i) for i in [1221, 121, 123, 10, -121]])
    s = Solution()
    print([s.isPalindrome2(i) for i in [1221, 121, 123, 10, -121]])
    print([s.isPalindrome3(i) for i in [1221, 121, 123, 10, -121]])
