# -*- coding: utf-8 -*-
# https://graphviz.readthedocs.io/en/stable/examples.html
# https://www.slideshare.net/sandpoonia/23-tree
# http://www.nct9.ne.jp/m_hiroi/light/pyalgo15.html

import sys
input = sys.stdin.readline
import graphviz
from collections import deque
import random


class Node:
    def __init__(self, val1, val2=None, left=None, mid=None, right=None, parent=None):
        self.val1 = val1
        self.val2 = val2
        self.left = left
        self.mid = mid
        self.right = right
        self.parent = parent
        self.viz_id = 0

    def is_leaf(self):
        return self.left is None and self.right is None

    def __str__(self):
        return f'{self.val1}:{self.val2}' if (self.val2 is not None) else f'{self.val1}'

    def is_2(self):
        return self.val2 is None

    def is_3(self):
        return self.val2 is not None

    def sibling(self):
        assert(self.parent.is_2())
        if self is self.parent.left:
            return self.parent.right
        else:
            return self.parent.left

    def align2(self, val):
        assert(self.val2 is None)
        self.val2 = val
        if self.val1 > self.val2:
            self.val1, self.val2 = self.val2, self.val1
        return

    def align3(self, val):
        assert(self.val2 is not None)
        if val < self.val1:
            val1 = self.val1
            self.val1 = val
            return val1
        elif val < self.val2:
            return val
        else:
            val2 = self.val2
            self.val2 = val
            return val2

    def divideAndConnect(self, node_l, node_r):
        if self.left.val1 == node_l.val1:
            assert(self.left.val2 == node_r.val1)
            node1, node2, node3, node4 = node_l, node_r, self.mid, self.right
        elif self.mid.val1 == node_l.val1:
            assert(self.mid.val2 == node_r.val1)
            node1, node2, node3, node4 = self.left, node_l, node_r, self.right
        elif self.right.val1 == node_l.val1:
            assert(self.right.val2 == node_r.val1)
            node1, node2, node3, node4 = self.left, self.mid, node_l, node_r
        else:
            raise Exception(
                "divideAndConnect has been called for non-parent node")

        new1 = Node(self.val1, None, node1, None, node2, None)
        new2 = Node(self.val2, None, node3, None, node4, None)

        node1.parent = node2.parent = new1
        node3.parent = node4.parent = new2

        return new1, new2

    def realignNode(self, node_l, node_r):
        if self.val2 > node_l.val1 and self.val2 > node_r.val1:
            node1, node2, node3 = node_l, node_r, self.right
        elif self.val1 < node_l.val1:
            node1, node2, node3 = self.left, node_l, node_r
        else:
            raise Exception("realignNode has wrong node_l and node_r values")

        self.left = node1
        self.mid = node2
        self.right = node3

        node1.parent = node2.parent = node3.parent = self

        return

    def successor(self, val2):
        if self.is_2():
            node = self.right
        elif self.is_3():
            if val2:
                node = self.right
            else:
                node = self.mid
        else:
            raise Exception("successor() is wrong")

        parent = None
        while node is not None:
            parent = node
            node = node.left

        return parent


class Tree23:
    def __init__(self):
        self.root = None
        self.g = None
        self.viz_index = 0

    def vis_node(self, node):
        if node.val2 is None:
            self.g.node(str(node.viz_id), label=f'{node.val1}', shape='square')
        else:
            self.g.node(str(node.viz_id), f'<l> {node.val1} | <r> {node.val2}')

    def vis_edge(self, node1, node2):
        if node1.is_leaf():
            return

        label_s = f'{node1.val1}:{node1.val2}' if (node1.val2 is not None) else f'{node1.val1}'
        if node2 is None:
            self.g.node(str(self.viz_index), shape="point")
            self.g.edge(str(node1.viz_id), str(self.viz_index),
                        style="dashed", label=label_s)
        else:
            self.g.edge(str(node1.viz_id), str(node2.viz_id), label=label_s)
            self.g.edge(str(node2.viz_id), str(
                node2.parent.viz_id), style="dashed")

    def find(self, query):
        node = self.root
        while node is not None:
            if query < node.val1:
                node = node.left
                continue
            if query is node.val1:
                return node
            if node.val2 is None:
                node = node.right
                continue
            if query < node.val2:
                node = node.mid
                continue
            if query is node.val2:
                return node
            node = node.right

        return None

    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
            return

        node = self.root
        parent = None
        while node is not None:
            parent = node
            if val < node.val1:
                node = node.left
                continue
            if val is node.val1:
                return
            if node.val2 is None:
                node = node.right
                continue
            if val < node.val2:
                node = node.mid
                continue
            if val is node.val2:
                return
            node = node.right

        node = parent
        # if node has only one elem, insert as the second elem
        if node.val2 is None:
            node.val2 = val
            if node.val1 > node.val2:
                node.val1, node.val2 = node.val2, node.val1
            return

        # node has two elems
        if node is self.root:
            # this happens at the very first stage
            l, m, r = sorted([val, node.val1, node.val2])
            l = Node(l)
            m = Node(m)
            r = Node(r)
            self.root = m
            m.left, m.right = l, r
            l.parent = r.parent = m
            return

        self._insert(parent, val)

    def _insert(self, node_, val):
        # node has two elems
        node = node_
        mid = val
        queue = deque()
        while node != self.root and node.val2 != None:
            queue.append(node)
            mid = node.align3(mid)
            node = node.parent

        if node is self.root and node.val2 is not None:
            mid = node.align3(mid)
            top = Node(mid)
            queue.append(node)
            node = queue.popleft()
            node_l, node_r = Node(node.val1), Node(node.val2)
            while len(queue) is not 0:
                parent = queue.popleft()
                node_l, node_r = parent.divideAndConnect(node_l, node_r)

            top.left, top.right = node_l, node_r
            node_l.parent = node_r.parent = top
            self.root = top
            return

        if node.val2 is None:
            node.align2(mid)
            top = node
            node = queue.popleft()
            node_l, node_r = Node(node.val1), Node(node.val2)
            while len(queue) is not 0:
                parent = queue.popleft()
                node_l, node_r = parent.divideAndConnect(node_l, node_r)

            top.realignNode(node_l, node_r)
            return

        else:
            raise Exception("Tree23._insert() has unexpected argument node_")
            return

    def delete(self, val):
        find = self.find(val)
        if not find:
            return

        delete = find
        if not find.is_leaf():
            suc = find.successor(val is find.val2)
            if find.is_2():
                find.val1, suc.val1 = suc.val1, find.val1,
                delete = suc
            elif find.is_3():
                if val is find.val1:
                    find.val1, suc.val1 = suc.val1, find.val1
                elif find.val2 and val is find.val2:
                    find.val2, suc.val1 = suc.val1, find.val2
                delete = suc

        # delete `delete`. `delete` is leaf
        if delete.is_3():
            if val is delete.val2:
                delete.val2 = None
                return
            else:
                delete.val1 = delete.val2
                delete.val2 = None
                return

        if delete is self.root:
            self.root = None
            return

        # `delete` is single node and parent is 2-elem node
        if delete.parent.is_3():
            # redistribution
            self.redistribute(delete.parent, delete)
            return

        # `delete` and parent(is_2) are both single
        # if sibling is 2-elem
        if delete.sibling().is_3():
            parent = delete.parent
            if delete is parent.right:
                delete.val1 = parent.val1
                parent.val1 = parent.left.val2
                parent.left.val2 = None
                return
            else:
                assert(delete is parent.left)
                right = parent.right
                delete.val1 = parent.val1
                parent.val1 = right.val1
                right.val1, right.val2 = right.val2, None
                return

        # `delete`, its parent, and its sibling are all single node
        node = delete.parent
        if delete is node.right:
            node.val1, node.val2 = node.left.val1, node.val1
            node.left = node.mid = node.right = None
        else:
            assert(delete is node.left)
            node.val2 = node.right.val1
            node.left = node.mid = node.right = None

        self.rebalance(node)

    def redistribute(self, node, delete):
        assert(node.is_3() and delete.is_leaf())
        if delete is node.left:
            if node.mid.val2 is not None:
                delete.val1 = node.val1
                node.val1 = node.mid.val1
                node.mid.val1 = node.mid.val2
                node.mid.val2 = None
                return
            else:
                delete.val1, delete.val2 = node.val1, node.mid.val1
                node.val1, node.val2 = node.val2, None
                node.mid = None
                return
        elif delete is node.mid:
            if node.left.val2 is not None:
                delete.val1 = node.val1
                node.val1 = node.left.val2
                node.left.val2 = None
                return
            else:
                node.left.val2 = node.val1
                node.val1, node.val2 = node.val2, None
                node.mid = None
                return
        else:
            assert(delete is node.right)
            if node.mid.val2 is not None:
                delete.val1, delete.val2 = node.val2, None
                node.val2 = node.mid.val2
                node.mid.val2 = None
                return
            else:
                delete.val1, delete.val2 = node.mid.val1, node.val2
                node.val2 = None
                node.mid = None
                return

    def rebalance(self, node):
        assert(node.is_3())
        while True:
            parent = node.parent
            if node is self.root:
                return
            if parent.is_3():
                break
            if node.sibling().is_3():
                break

            node = self.merge(parent, node)

        if parent.is_3():
            if node is parent.left:
                mid = parent.mid
                if mid.is_3():
                    new_l = Node(parent.val1)
                    node_l, node_m, node_r = mid.left, mid.mid, mid.right
                    parent.val1 = mid.val1
                    mid.val1, mid.val2 = mid.val2, None
                    mid.left, mid.mid, mid.right = node_m, None, node_r
                    parent.left, new_l.parent = new_l, parent
                    new_l.left, node.parent = node, new_l
                    new_l.right, node_l.parent = node_l, new_l
                    return
                if mid.is_2():
                    mid.right, mid.mid = mid.right, mid.left
                    mid.val1, mid.val2 = parent.val1, mid.val1
                    mid.left, node.parent = node, mid
                    parent.val1, parent.val2 = parent.val2, None
                    parent.left, parent.mid = parent.mid, None
                    return

            elif node is parent.mid:
                right = parent.right
                if right.is_3():
                    node_l, node_m, node_r = right.left, right.mid, right.right
                    new_m = Node(parent.val2)
                    parent.val2 = right.val1
                    right.val1, right.val2 = right.val2, None
                    right.left, right.mid, right.right = node_m, None, node_r
                    parent.mid, new_m.parent = new_m, parent
                    new_m.left, node.parent = node, new_m
                    new_m.right, node_l.parent = node_l, new_m
                    return
                if right.is_2():
                    right.right, right.mid = right.right, right.left
                    right.left, node.parent = node, right
                    right.val1, right.val2 = parent.val2, right.val1
                    parent.val2 = None
                    parent.mid = None
                    return

            elif node is parent.right:
                mid = parent.mid
                if mid.is_3():
                    node_l, node_m, node_r = mid.left, mid.mid, mid.right
                    new_r = Node(parent.val2)
                    parent.val2 = mid.val2
                    mid.val2 = None
                    parent.right, new_r.parent = new_r, parent
                    mid.mid, mid.right = None, node_m
                    new_r.right, node.parent = node, new_r
                    new_r.left, node_r.parent = node_r, new_r
                    return
                if mid.is_2():
                    mid.mid = mid.right
                    mid.right, node.parent = node, mid
                    mid.val2 = parent.val2
                    parent.val2 = None
                    parent.right, parent.mid = parent.mid, None
                    return
            else:
                print("Unexpected case in parent.is_3()")
                return

        if node.sibling().is_3():
            parent = node.parent
            if node is parent.right:
                sibling = parent.left
                node_l, node_m, node_r = sibling.left, sibling.mid, sibling.right
                new_r = Node(parent.val1)
                parent.right, new_r.parent = new_r, parent
                new_r.left, node_r.parent = node_r, new_r
                new_r.right, node.parent = node, new_r
                parent.val1 = sibling.val2
                sibling.val2 = None
                sibling.right, sibling.mid = sibling.mid, None
                return
            else:
                assert(node is parent.left)
                sibling = parent.right
                node_l, node_m, node_r = sibling.left, sibling.mid, sibling.right
                new_l = Node(parent.val1)
                parent.left, new_l.parent = new_l, parent
                new_l.left, node.parent = node, new_l
                new_l.right, node_l.parent = node_l, new_l
                parent.val1 = sibling.val1
                sibling.val1, sibling.val2 = sibling.val2, None
                sibling.left, sibling.mid = sibling.mid, None
                return

    def merge(self, node, child2):
        assert(child2.parent is node)
        # child2 is 2-elem, and node & sibling are both single
        # merge node and sibling
        if child2 is node.right:
            assert(node.left.is_2())
            node.val1, node.val2 = node.left.val1, node.val1
            node_l, node_r = node.left.left, node.left.right
            node.left, node_l.parent = node_l, node
            node.mid, node_r.parent = node_r, node
            return node
        else:
            assert(child2 is node.left and node.right.is_2())
            node.val2 = node.right.val1
            node_l, node_r = node.right.left, node.right.right
            node.mid, node_l.parent = node_l, node
            node.right, node_r.parent = node_r, node
            return node

    def view(self):
        self.g = graphviz.Digraph('structs', node_attr={'shape': 'record'})
        queue = deque()
        self.viz_index = 0
        self.root.viz_id = self.viz_index
        queue.append(self.root)
        # BFS
        while len(queue) is not 0:
            node = queue.pop()
            self.vis_node(node)
            # left
            self.viz_index += 1
            if node.left:
                node.left.viz_id = self.viz_index
                queue.append(node.left)
            self.vis_edge(node, node.left)
            # middle
            if node.mid:
                self.viz_index += 1
                node.mid.viz_id = self.viz_index
                queue.append(node.mid)
                self.vis_edge(node, node.mid)
            # right
            self.viz_index += 1
            if node.right:
                node.right.viz_id = self.viz_index
                queue.append(node.right)
            self.vis_edge(node, node.right)

        self.g.view()


def main():
    tree = Tree23()
    size = 100
    values = random.sample(range(0, 200), size)

    deletes = random.sample(values, int(size*3/4))

    with open('inputs.txt', 'w') as f:
        for i in values:
            f.write(str(i) + '\n')

    with open('deletes.txt', 'w') as f:
        for i in deletes:
            f.write(str(i) + '\n')

    for i in values:
        tree.insert(i)

    for i in deletes:
        tree.delete(i)

    while True:
        inputs = list(input().split())
        if len(inputs) == 1:
            cmd = str(inputs[0])
            if cmd == 'q' or cmd == 'quit':
                break
            elif cmd == 'view':
                tree.view()
            else:
                print("type 'q' or 'quit' or 'view'")
        elif len(inputs) == 2:
            cmd = str(inputs[0])
            x = int(inputs[1])
            if cmd == 'insert':
                tree.insert(x)
            elif cmd == 'delete':
                tree.delete(x)
            else:
                print("type 'insert x' or 'delete x'")


def debug():
    tree = Tree23()
    with open('inputs_example.txt') as f:
        for s in f:
            tree.insert(int(s))

    with open('deletes_example.txt') as f:
        for s in f:
            tree.delete(int(s))

    while True:
        inputs = list(input().split())
        if len(inputs) == 1:
            cmd = str(inputs[0])
            if cmd == 'q' or cmd == 'quit':
                break
            elif cmd == 'view':
                tree.view()
            else:
                print("type 'q' or 'quit' or 'view'")
        elif len(inputs) == 2:
            cmd = str(inputs[0])
            x = int(inputs[1])
            if cmd == 'insert':
                tree.insert(x)
            elif cmd == 'delete':
                tree.delete(x)
            else:
                print("type 'insert x' or 'delete x'")

    return


if __name__ == '__main__':
    main()
    # debug()
