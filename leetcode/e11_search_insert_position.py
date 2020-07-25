# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:搜索插入位置
@time:2020/4/3 21:32
"""
'''
给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。
如果目标值不存在于数组中，返回它将会被按顺序插入的位置。
'''
"""
你可以假设数组中无重复元素。

示例 1:
输入: [1,3,5,6], 5
输出: 2

示例 2:
输入: [1,3,5,6], 2
输出: 1

示例 3:
输入: [1,3,5,6], 7
输出: 4

示例 4:
输入: [1,3,5,6], 0
输出: 0
"""
from typing import List


class Solution:
    # 类似指针法，从前往后，一个一个对比，时间复杂度O(n)
    def searchInsert(self, nums: List[int], target: int) -> int:
        index = 0
        len_nums = len(nums)
        while index < len_nums:
            if target == nums[index] or target < nums[index]:
                return index
            index += 1
        return len_nums

    # 利用Python的in，若没有找到，就放到nums中排序再返回target下标
    def searchInsert1(self, nums: List[int], target: int) -> int:
        if target in nums:
            return nums.index(target)
        nums.append(target)
        nums.sort()
        return nums.index(target)

    # 二分法，看了别人写的思路，然后默写
    def searchInsert2(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:  # 想了下，为啥要加=号，通过debug才发现到
            mid = (left + right) >> 1
            mid_var = nums[mid]
            if mid_var == target:
                return mid
            elif mid_var < target:
                left = mid + 1
            else:
                right = mid - 1
        return left


if __name__ == '__main__':
    s = Solution()
    li = [1, 3, 5, 6]
    print([s.searchInsert(li, target) for target in [5, 2, 7, 0]])
    print([s.searchInsert2(li, target) for target in [5, 2, 7, 0]])
