# -*- coding: utf-8 -*-
# https://graphviz.readthedocs.io/en/stable/examples.html

import sys
input = sys.stdin.readline
import graphviz
from collections import deque

class Node:
    def __init__(self, val1, val2, left, mid, right):
        self.val1 = val1
        self.val2 = val2
        self.left = left
        self.mid = mid
        self.right = right
        self.viz_id = 0

    def is_leaf(self):
        return self.left is None and self.right is None

    def __str__(self):
        return f'{self.val1}:{self.val2}' if (self.val2 is not None) else f'{self.val1}'
    
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

    def example(self):
        node1 = Node(10, None, None, None, None)
        node3 = Node(30, None, None, None, None)
        node5 = Node(50, None, None, None, None)
        node7 = Node(70, None, None, None, None)
        node9_10 = Node(90, 100, None, None, None)

        node2 = Node(20, None, node1, None, node3)
        node6_8 = Node(60, 80, node5, node7, node9_10)
        node4 = Node(40, None, node2, None, node6_8)

        self.root = node4

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
        else:
            print("node to be inserted has two values, skipping")
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
    tree.example()
    for i in [10, 30, 50, 70, 90]:
        print(tree.find(i))

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
                tree.insert(x)
            else:
                print("type 'insert x'")
    
