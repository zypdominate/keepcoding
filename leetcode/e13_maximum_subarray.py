# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:最大子序和
@time:2020/4/9 20:00
"""
"""
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

示例:
输入: [-2,1,-3,4,-1,2,1,-5,4],
输出: 6
解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。
进阶:

如果你已经实现复杂度为 O(n) 的解法，尝试使用更为精妙的分治法求解。
"""

from typing import List


class Solution:
    # leetcode上，当测试数据较大时，会出现超时
    def maxSubArray0(self, nums: List[int]) -> int:
        length = len(nums)
        if length == 1:
            return nums[0]
        i = 0
        res_max = nums[0]
        while i < length:
            j = i + 1
            while j < length + 1 and i <= j:
                crt_max = sum(nums[i:j])
                j += 1
                res_max = crt_max if res_max < crt_max else res_max
            i += 1
        return res_max

    # 暴力解法2:穷举所有的子区间(时间复杂度：O(N^2)，空间复杂度O(1))
    def maxSubArray1(self, nums: List[int]) -> int:
        length = len(nums)
        res = nums[0]
        for i in range(length):
            sum = 0
            for j in range(i + 1, length):
                sum += nums[j]
                res = max(sum, res)
        return res

    # 动态规划法
    def maxSubArray2(self, nums: List[int]) -> int:
        """
        对于每一个数，若前面的子数组和为正，则加上前面的子数组作为新的子数组，若为负则保留自身作为新的子数组；
        每次遍历都与当前最大子数组和做比较，保留较大者。
        """
        realmax = submax = nums[0]
        for i in nums[1:]:
            if submax > 0:
                submax += i
            else:
                submax = i
            realmax = max(realmax, submax)
        return realmax

    # Kadane算法（贪心）: 和上面的动态规划方法思路很像
    def maxSubArray3(self, nums: List[int]) -> int:
        realmax = submax = nums[0]
        for i in nums:
            submax = max(i, submax + i)
            realmax = max(realmax, submax)
        return realmax

    # 分治法：在leetcode上测试，发现竟然超时了.....
    def maxSubArray(self, nums: List[int]) -> int:
        def maxSubArrayDivideWithBorder(nums, start, end):
            # 1. 递归的结束出口：只有一个元素，
            if start == end:
                return nums[start]

            # 2. 计算中间值、左侧子序列最大值、右侧子序列最大值
            center = (start + end) // 2
            leftMax = maxSubArrayDivideWithBorder(nums, start, center)
            rightMax = maxSubArrayDivideWithBorder(nums, center + 1, end)

            # 3. 计算横跨中心位置的两个子序列的最大值
            leftCrossSum = 0
            leftCrossMax = nums[center]
            for i in range(center, -1, -1):  # 以center下标开始，逆序求和
                leftCrossSum += nums[i]
                leftCrossMax = max(leftCrossMax, leftCrossSum)

            rightCrossSum = 0
            rightCrossMax = nums[center + 1]
            for i in range(center + 1, len(nums)):  # 以center+1下标开始，顺序求和
                rightCrossSum += nums[i]
                rightCrossMax = max(rightCrossMax, rightCrossSum)
            crossMax = leftCrossMax + rightCrossMax

            # 4. 计算最大值：比较左侧子序列、右侧子序列、横跨子序列三者的最值
            return max(crossMax, max(leftMax, rightMax))

        return maxSubArrayDivideWithBorder(nums, 0, len(nums) - 1)


if __name__ == '__main__':
    s = Solution()
    print(s.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
    print(s.maxSubArray([-2, -1]))
    print(s.maxSubArray([1, -1, 1]))
