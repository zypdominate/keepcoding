'''
两数之和
给定一个整数数组 nums 和一个目标值 target，
请你在该数组中找出和为目标值的那 两个 整数，
并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。
'''
from typing import List

"""
给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
"""


def twoSum(nums: List[int], target: int) -> List[int]:
    length = len(nums)
    for i in range(length):
        for j in range(i + 1, length):
            if nums[i] + nums[j] == target:
                return [i, j]


def twoSum2(nums, target):
    lens = len(nums)
    j = -1
    for i in range(lens):
        if (target - nums[i]) in nums:
            if (nums.count(target - nums[i]) == 1) & (
                    target - nums[i] == nums[i]):  # 如果num2=num1,且nums中只出现了一次，说明找到是num1本身。
                continue
            else:
                j = nums.index(target - nums[i], i + 1)  # index(x,i+1)是从num1后的序列后找num2
                break
    if j > 0:
        return [i, j]
    else:
        return []


def twoSum3(nums, target):
    lens = len(nums)
    j = -1
    for i in range(1, lens):
        temp = nums[:i]
        if (target - nums[i]) in temp:
            j = temp.index(target - nums[i])
            break
    if j >= 0:
        return [j, i]


if __name__ == '__main__':
    nums = [3, 2, 3, 4]
    target = 6
    print(twoSum(nums, target))
    print(twoSum2(nums, target))
    print(twoSum3(nums, target))
