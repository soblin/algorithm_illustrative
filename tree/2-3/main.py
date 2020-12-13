# -*- coding: utf-8 -*-
# https://graphviz.readthedocs.io/en/stable/examples.html

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
            print("Error in divideAndConnect")
            return
        
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
            print("Error in divideAndConnect")
            return

        self.left = node1
        self.mid = node2
        self.right = node3

        node1.parent = node2.parent = node3.parent = self
        
        return
    
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
            self.g.edge(str(node1.viz_id), str(self.viz_index), style="dashed", label=label_s)
        else:
            self.g.edge(str(node1.viz_id), str(node2.viz_id), label=label_s)
            self.g.edge(str(node2.viz_id), str(node2.parent.viz_id), style="dashed")
            
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

    def insert(self, val, aux=False):
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

        if aux:
            self._insert2(parent, val)
        else:
            self._insert1(parent, val)
        
    def _insert1(self, node, val):
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

        parent = node.parent # this is not None, because node is not root
        if parent.val2 is None:
            l, m, r = sorted([val, node.val1, node.val2])
            l = Node(l)
            r = Node(r)
            if val < parent.val1:
                parent.val2 = m
                if parent.val1 > parent.val2:
                    parent.val1, parent.val2 = parent.val2, parent.val1
                parent.left = l
                l.parent = parent
                parent.mid = r
                r.parent = parent
            else:
                parent.val2 = m
                parent.mid = l
                l.parent = parent
                parent.right = r
                r.parent = parent
            return
        if parent is self.root:
            if node is parent.left:
                l, m, r = sorted([val, node.val1, node.val2])
                ch_l = Node(l)
                ch_r = Node(r)
                l, m, r = sorted([m, parent.val1, parent.val2])
                # make parent 1-elem node
                parent.val1, parent.val2 = r, None
                parent.left = parent.mid
                parent.mid = None
                pa_l = Node(l)
                pa_l.left, ch_l.parent = ch_l, pa_l
                pa_l.right, ch_r.parent = ch_r, pa_l
                self.root = Node(m)
                self.root.left, pa_l.parent = pa_l, self.root
                self.root.right, parent.parent = parent, self.root
                return
            elif node is parent.mid:
                l, m, r = sorted([val, node.val1, node.val2])
                ch_l = Node(l)
                ch_r = Node(r)
                l, m, r = sorted([m, parent.val1, parent.val2])
                pa_l = Node(l)
                pa_l.left = parent.left
                parent.left.parent = pa_l
                pa_l.right = ch_l
                ch_l.parent = pa_l
                pa_r = Node(r)
                pa_r.right = parent.right
                parent.right.parent = pa_r
                pa_r.left = ch_r
                ch_r.parent = pa_r
                self.root = Node(m)
                self.root.left = pa_l
                pa_l.parent = self.root
                self.root.right = pa_r
                pa_r.parent = self.root
                return
            elif node is parent.right:
                l, m, r = sorted([val, node.val1, node.val2])
                ch_l = Node(l)
                ch_r = Node(r)
                pa_r = Node(m)
                pa_r.left, ch_l.parent = ch_l, pa_r
                pa_r.right, ch_r.parent = ch_r, pa_r
                parent.right = parent.mid
                parent.mid = None
                self.root = Node(parent.val2)
                parent.val2 = None
                self.root.left = parent
                parent.parent = self.root
                self.root.right = pa_r
                pa_r.parent = self.root
                return
        else:
            print("unexpected case")
        return

    def _insert2(self, node_, val):
        # node has two elems
        node = node_
        mid = val
        queue = deque()
        while node != self.root and node.val2 != None:
            queue.append(node)
            mid = node.align3(mid)
            node = node.parent

        if node is self.root and node.val2 is not None:
            print("in _insert2, node is self.root and node.val2 is not None")
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
            print("in _insert2, node.val2 is None")
            # queue.append(node)
            node = queue.popleft()
            node_l, node_r = Node(node.val1), Node(node.val2)
            while len(queue) is not 0:
                parent = queue.popleft()
                print(f"queue.pop is {parent}")
                node_l, node_r = parent.divideAndConnect(node_l, node_r)

            top.realignNode(node_l, node_r)
            return
        
        else:
            print("in _insert2, else")
            return
        
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
        
if __name__ == '__main__':
    tree = Tree23()
    # values = random.sample(range(0, 100), 40)
    values = [27, 5, 21, 65, 96, 1, 2, 14, 15, 24, 25, 55, 56, 68, 70, 97, 98, 22, 0, 3, 16]
    for i in values:
        tree.insert(i)
    
    while True:
        inputs = list(input().split())
        if len(inputs) == 1:
            cmd = str(inputs[0])
            if cmd == 'q' or cmd == 'quit':
                exit()
            elif cmd == 'view':
                tree.view()
            else:
                print("type 'q' or 'quit' or 'view'")
        elif len(inputs) == 2:
            cmd = str(inputs[0])
            x = int(inputs[1])
            if cmd == 'insert':
                tree.insert(x, True)
            else:
                print("type 'insert x'")
    
