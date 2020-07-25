from nose.tools import assert_equal


class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def __str__(self):
        return str(self.data)


class LinkedList(object):
    def __init__(self, head=None):
        self.head = head

    # 计算链表长度
    def __len__(self):
        crt_node = self.head
        counter = 0
        while crt_node is not None:
            counter += 1
            crt_node = crt_node.next
        return counter

    # 从前插入
    def insert_to_front(self, data):
        if data is None:
            return None
        else:
            node = Node(data, self.head)
            self.head = node
            return node

    # 从后插入
    def append(self, data):
        if data is None:
            return None
        node = Node(data)
        if self.head is None:
            self.head = node
            return node
        else:
            crt_node = self.head
            while crt_node.next is not None:
                crt_node = crt_node.next
            crt_node.next = node
        return node

    # 查找
    def find(self, data):
        if data is None:
            return None
        else:
            crt_node = self.head
            while crt_node is not None:
                if crt_node.data == data:
                    return crt_node
                else:
                    crt_node = crt_node.next
            return None

    # 删除:方法一
    def delete(self, data):
        if data is None or self.head is None:
            return None
        else:
            if self.head.data == data:
                self.head = self.head.next
            else:
                pre_node = self.head
                crt_node = self.head.next
                while crt_node is not None:
                    if crt_node.data == data:
                        pre_node.next = crt_node.next
                        # return None # 若这里直接返回，就只删除第一个找到的等于data的node
                        crt_node = crt_node.next  # 加上这行可以删除所有匹配的
                    else:
                        pre_node = crt_node
                        crt_node = crt_node.next
                return None

    # 删除:方法二
    def delete2(self, data):
        if data is None or self.head is None:
            return None
        else:
            if self.head.data == data:
                self.head = self.head.next
            else:
                crt_node = self.head
                while crt_node.next is not None:
                    if crt_node.next.data == data:
                        crt_node.next = crt_node.next.next
                    else:
                        crt_node = crt_node.next
            return None

    # 打印输出
    def print_data(self):
        crt_node = self.head
        while crt_node is not None:
            print(crt_node.data)
            crt_node = crt_node.next

    # 获取所有data
    def get_all_data(self):
        get_data = []
        crt_node = self.head
        while crt_node is not None:
            get_data.append(crt_node.data)
            crt_node = crt_node.next
        return get_data


class TestLinkedList(object):

    def test_insert_to_front(self):
        linked_list = LinkedList(None)

        print('Test: insert_to_front on an empty list')
        linked_list.insert_to_front(10)
        assert_equal(linked_list.get_all_data(), [10])

        print('Test: insert_to_front on a None')
        linked_list.insert_to_front(None)
        assert_equal(linked_list.get_all_data(), [10])

        print('Test: insert_to_front general case')
        linked_list.insert_to_front('a')
        linked_list.insert_to_front('bc')
        assert_equal(linked_list.get_all_data(), ['bc', 'a', 10])

        print('Success: test_insert_to_front\n')

    def test_append(self):
        linked_list = LinkedList(None)

        print('Test: append on an empty list')
        linked_list.append(10)
        assert_equal(linked_list.get_all_data(), [10])

        print('Test: append a None')
        linked_list.append(None)
        assert_equal(linked_list.get_all_data(), [10])

        print('Test: append general case')
        linked_list.append('a')
        linked_list.append('bc')
        assert_equal(linked_list.get_all_data(), [10, 'a', 'bc'])

        print('Success: test_append\n')

    def test_find(self):
        print('Test: find on an empty list')
        linked_list = LinkedList(None)
        node = linked_list.find('a')
        assert_equal(node, None)

        print('Test: find a None')
        head = Node(10)
        linked_list = LinkedList(head)
        node = linked_list.find(None)
        assert_equal(node, None)

        print('Test: find general case with matches')
        head = Node(10)
        linked_list = LinkedList(head)
        linked_list.insert_to_front('a')
        linked_list.insert_to_front('bc')
        node = linked_list.find('a')
        assert_equal(str(node), 'a')

        print('Test: find general case with no matches')
        node = linked_list.find('aaa')
        assert_equal(node, None)

        print('Success: test_find\n')

    def test_delete(self):
        print('Test: delete on an empty list')
        linked_list = LinkedList(None)
        linked_list.delete('a')
        assert_equal(linked_list.get_all_data(), [])

        print('Test: delete a None')
        head = Node(10)
        linked_list = LinkedList(head)
        linked_list.delete(None)
        assert_equal(linked_list.get_all_data(), [10])

        print('Test: delete general case with matches')
        head = Node(10)
        linked_list = LinkedList(head)
        linked_list.insert_to_front('a')
        linked_list.insert_to_front('a')
        linked_list.insert_to_front('bc')
        linked_list.delete('a')
        assert_equal(linked_list.get_all_data(), ['bc', 10])

        print('Test: delete general case with no matches')
        linked_list.delete('aa')
        assert_equal(linked_list.get_all_data(), ['bc', 10])

        print('Success: test_delete\n')

    def test_len(self):
        print('Test: len on an empty list')
        linked_list = LinkedList(None)
        assert_equal(len(linked_list), 0)

        print('Test: len general case')
        head = Node(10)
        linked_list = LinkedList(head)
        linked_list.insert_to_front('a')
        linked_list.insert_to_front('bc')
        assert_equal(len(linked_list), 3)

        print('Success: test_len\n')


def main():
    test = TestLinkedList()
    test.test_insert_to_front()
    test.test_append()
    test.test_find()
    test.test_delete()
    test.test_len()


if __name__ == '__main__':
    main()
