class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def __str__(self):
        return str(self.data)


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

node1.next = node2
node2.next = node3
print(node1, node1.next)  # 1 2
print(node2, node2.next)  # 2 3
print(node3, node3.next)  # 3 None


# 在使用链表时常用到while循环
def printLinkedList(node):
    while node:
        print(node)
        node = node.next


printLinkedList(node1)


# 递归打印
def recursiveprintLinkedList(node):
    if node is None:
        return None
    head = node
    tail = node.next
    print(head, tail)
    recursiveprintLinkedList(tail)
    print(head, tail)


recursiveprintLinkedList(node1)


# 简化递归：
def recursiveprintLinkedList2(node):
    if node is None:
        return None
    print(node)
    return recursiveprintLinkedList2(node.next)


recursiveprintLinkedList2(node1)

