#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Description:二分法查找
# Author:zhuyuping
# datetime:2020/8/10 23:27
import random


def binary_search(listarr, target):
    low = 0
    high = len(listarr) - 1
    count = 1
    while low <= high:
        mid = (low + high) >> 1
        guess = listarr[mid]
        if guess == target:
            print(f'by search {count} times, index of target num {target} is {mid}')
            return mid
        if guess < target:
            low = mid + 1
        else:
            high = mid - 1
        count += 1
    return None


if __name__ == '__main__':
    # 随机生成一个有序的列表，
    test_list = sorted([random.randint(1, 100) for i in range(10)])
    print(test_list)
    # 在有序随机列表中，随机挑选一个数字，用二分法找到其下标
    binary_search(test_list, random.choice(test_list))
