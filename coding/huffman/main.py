# -*- coding: utf-8 -*-
import sys
input = sys.stdin.readline
from queue import PriorityQueue as PQueue
from collections import deque
import graphviz

class Node:
    def __init__(self, c, n):
        self.c = c
        self.num = n
        self.left = None
        self.right = None
        self.code = None
        self.viz_id = 0
        
    def __lt__(self, rhs):
        """self < rhs"""
        return self.num < rhs.num

    def __le__(self, rhs):
        """self <= rhs"""
        return self.num <= rhs.num

    def __eq__(self, rhs):
        return self.num == rhs.num

    def __neq__(self, rhs):
        return self.num != rhs.num

    def __gt(self, rhs):
        return self.num > rhs.num

    def __ge__(self, rhs):
        return self.num >= rhs.num

    def __str__(self):
        if self.c is not None:
            return f'Leaf {self.c}:{self.num}'
        else:
            return f'Node: {self.num}'

    def is_leaf(self):
        return self.left is None and self.right is None
    
class HuffmanTree:
    def __init__(self):
        self.nodes = []
        self.root = None

    def insert(self, node):
        self.nodes.append(node)

    def encode(self):
        self._encode(self.root, "")

    def _encode(self, node, c):
        if node.is_leaf():
            node.code = c
            return
        else:
            self._encode(node.left, c+"0")
            self._encode(node.right, c+"1")
            return

    def view(self):
        g = graphviz.Digraph()
        queue = deque()
        viz_index = 0
        self.root.viz_id = viz_index
        queue.append(self.root)
        # BFS
        while len(queue) is not 0:
            node = queue.pop()
            if node.is_leaf():
                g.node(str(node.viz_id), label=f'{node.c}({node.num})\n{node.code}', shape="square")
            elif node.c is None:
                g.node(str(node.viz_id), label=f'{node.num}', shape="circle")
            else:
                continue

            # add edge
            if not node.is_leaf():
                viz_index += 1
                node.left.viz_id = viz_index
                queue.append(node.left)
                g.edge(str(node.viz_id), str(node.left.viz_id), label="0")
                viz_index += 1
                node.right.viz_id = viz_index
                queue.append(node.right)
                g.edge(str(node.viz_id), str(node.right.viz_id), label="1")

        g.view()
    
if __name__ == '__main__':
    n_char = int(input())
    nodes = []
    queue = PQueue()
    for _ in range(n_char):
        inputs = list(input().split())
        c = str(inputs[0])
        n = int(inputs[1])
        queue.put(Node(c, n))

    tree = HuffmanTree()
    while queue.qsize() is not 0:
        if queue.qsize() is 1:
            # last
            tree.root = queue.get()
            break
        else:
            min1 = queue.get()
            min2 = queue.get()
            tree.insert(min1)
            tree.insert(min2)
            node = Node(None, min1.num + min2.num)
            node.left = min1
            node.right = min2
            queue.put(node)

    tree.encode()
    tree.view()
