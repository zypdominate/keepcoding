#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Description:选择排序
# Author:zhuyuping
# datetime:2020/8/11 22:31
import random


def find_smallest(arr):
    smallest = arr[0]
    smallest_index = 0
    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_index = i
    return smallest_index


def select_sort(arr):
    res = []
    for i in range(len(arr)):
        smallest = find_smallest(arr)
        res.append(arr.pop(smallest))
    return res


if __name__ == '__main__':
    arr = [random.randint(1, 100) for i in range(10)]
    print(select_sort(arr))
