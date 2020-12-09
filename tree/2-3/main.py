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
        node1 = Node(1, None, None, None, None)
        node3 = Node(3, None, None, None, None)
        node5 = Node(5, None, None, None, None)
        node7 = Node(7, None, None, None, None)
        node9_10 = Node(9, 10, None, None, None)

        node2 = Node(2, None, node1, None, node3)
        node6_8 = Node(6, 8, node5, node7, node9_10)
        node4 = Node(4, None, node2, None, node6_8)

        self.root = node4
        
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
    tree.view()
