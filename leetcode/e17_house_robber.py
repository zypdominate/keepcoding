# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:
@time:2020/5/29 18:18
"""
'''
你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，
如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。
给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。

示例 1:
输入: [1,2,3,1]
输出: 4
解释: 偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
     偷窃到的最高金额 = 1 + 3 = 4 。

示例 2:
输入: [2,7,9,3,1]
输出: 12
解释: 偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
     偷窃到的最高金额 = 2 + 9 + 1 = 12 。
'''

from typing import List
from functools import lru_cache
import time


# 计时
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        res = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        args_str = ', '.join(repr(arg) for arg in args)
        print(f'[{elapsed:>2.8}s], {name}({args_str})--> {res}')
        return res

    return clocked


@lru_cache()
@clock
def dp(nums, i):
    if i == 0:
        return nums[0]
    elif i == 1:
        return max(nums[1], nums[0])
    return max(dp(nums, i - 1), dp(nums, i - 2) + nums[i])


class Solution:
    # 递归
    def rob(self, nums: List[int]) -> int:
        nums = tuple(nums)  # 配合用lru_cache时，不能处理列表
        if not nums:
            return 0
        return dp(nums, len(nums) - 1)

    # 动态规划
    def rob2(self, nums: List[int]) -> int:
        if not nums:
            return 0
        length = len(nums)
        dp = [0] * length
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, length):
            dp[i] = max(dp[i - 2] + nums[i], dp[i - 1])
        return dp[length - 1]

    # 滚动数组
    def rob3(self, nums: List[int]) -> int:
        if not nums:
            return 0
        length = len(nums)
        if length == 1:
            return nums[0]
        first, second = nums[0], max(nums[0], nums[1])
        for i in range(2, length):
            first, second = second, max(first + nums[i], second)
        print(second)
        return second


if __name__ == '__main__':
    s = Solution()
    assert s.rob([1, 2, 3, 1]) == s.rob2([1, 2, 3, 1]) == s.rob3([1, 2, 3, 1])
    assert s.rob([2, 7, 9, 3, 1]) == s.rob2([2, 7, 9, 3, 1]) == s.rob3([2, 7, 9, 3, 1])
