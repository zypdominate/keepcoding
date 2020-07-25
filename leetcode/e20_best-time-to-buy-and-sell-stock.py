#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:zhuyuping
# datetime:2020/7/12 13:41
"""
给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
如果你最多只允许完成一笔交易（即买入和卖出一支股票一次），设计一个算法来计算你所能获取的最大利润。
注意：你不能在买入股票前卖出股票。

示例 1:
输入: [7,1,5,3,6,4]
输出: 5
解释: 在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。

示例 2:
输入: [7,6,4,3,1]
输出: 0
解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。
"""
from typing import List


class Solution:
    # 自己写的动态规划，结果在网页上timeout，思路应该是对的
    def maxProfit(self, prices: List[int]) -> int:
        length = len(prices)
        profit = 0
        for i in range(length):
            for j in range(i + 1, length):
                profit = max(profit, prices[j] - prices[i])
        return profit

    # 一次遍历，时间复杂度O(n)，空间复杂度O(1)
    def maxProfit2(self, prices: List[int]) -> int:
        min_price = prices[0] if prices else 0
        max_profit = 0
        for i in range(1, len(prices)):
            curr_price = prices[i]
            curr_profit = curr_price - min_price
            # 当前价格小于历史最低时，设置历史最低价格为当前价格；
            if curr_price < min_price:
                min_price = curr_price
            # 当前获得利润大于历史最大利润时，设置历史最大利润为当前利润；
            elif curr_profit > max_profit:
                max_profit = curr_profit
        return max_profit

    # 对maxProfit2优化
    def maxProfit21(self, prices: List[int]) -> int:
        min_price = prices[0] if prices else 0
        max_profit = 0
        for price in prices:
            max_profit = max(max_profit, price - min_price)
            min_price = min(min_price, price)
        return max_profit


if __name__ == '__main__':
    s = Solution()
    print(s.maxProfit2([7, 1, 5, 3, 6, 4]))
    print(s.maxProfit2([7, 6, 4, 3, 1]))
    print(s.maxProfit2([7, 6, 4, 3, 1, 2]))
