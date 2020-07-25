# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:移除元素
@time:2020/3/30 18:10
"""
'''
给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素，并返回移除后数组的新长度。
不要使用额外的数组空间，你必须仅使用 O(1) 额外空间并 原地 修改输入数组。
元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。
'''
"""
示例 1:
给定 nums = [3,2,2,3], val = 3,
函数应该返回新的长度 2, 并且 nums 中的前两个元素均为 2。
你不需要考虑数组中超出新长度后面的元素。

示例 2:
给定 nums = [0,1,2,2,3,0,4,2], val = 2,
函数应该返回新的长度 5, 并且 nums 中的前五个元素为 0, 1, 3, 0, 4。
注意这五个元素可为任意顺序。
你不需要考虑数组中超出新长度后面的元素。
"""
# 本题和 easy8_remove_duplicates_from_sorted_array.py 有点像
from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        p = 0
        while p < len(nums):
            if nums[p] == val:
                nums.remove(val)
                p -= 1
            p += 1
        return len(nums)

    # 看到一种比较奇特的思路: 重新梳理nums，像指针
    def removeElement2(self, nums: List[int], val: int) -> int:
        p = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[p] = nums[i]
                p += 1
        return p  # 需要注意的是，最后返回不是nums的长度


if __name__ == '__main__':
    s = Solution()
    assert s.removeElement2([1], 1) == 0
    assert s.removeElement2([3, 2, 2, 3], 3) == 2
    assert s.removeElement2([0, 1, 2, 2, 3, 0, 4, 2], 2) == 5
