#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:zhuyuping
# datetime:2020/7/12 1:15
"""
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
注意：给定 n 是一个正整数。

示例 1：
输入： 2
输出： 2
解释： 有两种方法可以爬到楼顶。
1.  1 阶 + 1 阶
2.  2 阶

示例 2：
输入： 3
输出： 3
解释： 有三种方法可以爬到楼顶。
1.  1 阶 + 1 阶 + 1 阶
2.  1 阶 + 2 阶
3.  2 阶 + 1 阶
"""
'''
爬到第n楼的方法，为爬到第n-1楼和n-2楼的方法之和
'''
from functools import lru_cache


class Solution:
    # 方法1:直接递归解法，容易超时，可以加个缓存装饰器
    @lru_cache()
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return self.climbStairs(n - 1) + self.climbStairs(n - 2)

    # 方法2：直接DP，新建一个字典或者数组来存储以前的变量，空间复杂度O(n)
    def climbStairs1(self, n: int) -> int:
        dp = {}
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]

    # DP，只存储前两个元素，减少了空间，空间复杂度O(1)
    # 可以理解成：自下而上的递归（递推）
    def climbStairs2(self, n: int) -> int:
        if n <= 2:
            return n
        a, b = 1, 2
        for i in range(2, n):
            a, b = b, a + b
        return b


if __name__ == '__main__':
    s = Solution()
    assert s.climbStairs2(2) == 2
    assert s.climbStairs2(3) == 3
    print(s.climbStairs2(4))
