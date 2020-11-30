# -*- coding: utf-8 -*-
import graphviz
from collections import deque

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.attr = None
        self.viz_id = None
        
class AVLTree:
    def __init__(self):
        self.root = None
        self.nodes = [] # cached the reference to nodes
 
    def insert(self, x):
        """
        allow duplicate id node
        """
        if self.root is None:
            self.root = Node(x)
            self.nodes.append(self.root)
            return

        node = self.root
        parent = None
        while node is not None:
            if x <= node.val:
                parent = node
                node = node.left
            else:
                parent = node
                node = node.right

        if x <= parent.val:
            node = Node(x)
            node.parent = parent
            node.attr = "left_child"
            parent.left = node
            self.nodes.append(node)
        else:
            node = Node(x)
            node.parent = parent
            node.attr = "right_child"
            parent.right = node
            self.nodes.append(node)

        return

    def view(self):
        g = graphviz.Graph()
        queue = deque()
        viz_index = 0
        self.root.viz_id = viz_index
        queue.append(self.root)
        while len(queue) is not 0:
            node = queue.pop()
            g.node(str(node.viz_id), label="{0}".format(node.val))
            if node.left is not None:
                viz_index += 1
                node.left.viz_id = viz_index
                queue.append(node.left)
                g.edge(str(node.viz_id), str(node.left.viz_id))

            if node.right is not None:
                viz_index += 1
                node.right.viz_id = viz_index
                queue.append(node.right)
                g.edge(str(node.viz_id), str(node.right.viz_id))

        g.view()

if __name__ == '__main__':
    tree = AVLTree()
    values = [7, 10, 11, 5, 3, 6, 1, 4, 13, 25, 12]
    for val in values:
        tree.insert(val)
    
    tree.view()
