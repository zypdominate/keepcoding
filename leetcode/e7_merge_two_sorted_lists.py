# -*- coding:utf-8 -*-
"""
@author:zhuyuping
@description:合并两个有序链表
@time:2020/3/27 12:27
"""
'''
将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。 

示例：
输入：1->2->4, 1->3->4
输出：1->1->2->3->4->4
'''


# Definition for singly-linked list.
class ListNode:
    def __init__(self, var):
        self.val = var
        self.next = None


class Solution2:
    def mergeTwoLists(self, l1, l2):
        # maintain an unchanging reference to node ahead of the return node.
        prehead = ListNode(-1)

        prev = prehead
        while l1 and l2:  # 两个链表都有值域时才比较
            if l1.val <= l2.val:
                prev.next = l1
                l1 = l1.next
            else:
                prev.next = l2
                l2 = l2.next
            prev = prev.next

        # exactly one of l1 and l2 can be non-null at this point, so connect
        # the non-null list to the end of the merged list.
        prev.next = l1 if l2 is None else l2
        return prehead.next


class Solution3:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if l1 is None:
            return l2  # 终止条件，直到两个链表都空
        elif l2 is None:
            return l1
        else:
            if l1.val < l2.val:
                l1.next = self.mergeTwoLists(l1.next, l2)
                return l1
            else:
                l2.next = self.mergeTwoLists(l1, l2.next)
                return l2


if __name__ == '__main__':
    s = Solution3()
    L1 = ListNode('1->2->4')
    L2 = ListNode('1->3->4')
    ret = s.mergeTwoLists(L1, L2)
