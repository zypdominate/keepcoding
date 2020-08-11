#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Description:
# Author:zhuyuping
# datetime:2020/8/11 23:56
import random


def quick_sort(arr):
    if arr == [] or len(arr) == 1:
        return arr
    base = arr[0]
    smaller_arr = []
    larger_arr = []
    for i in arr[1::]:  # 取出作为base的元素
        if i < base:
            smaller_arr.append(i)
        else:
            larger_arr.append(i)
    return quick_sort(smaller_arr) + [base] + quick_sort(larger_arr)


if __name__ == '__main__':
    arr = [random.randint(1, 100) for i in range(10)]
    print(quick_sort(arr))
