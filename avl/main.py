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

    def delete(self, query):
        node = self.root
        while node is not None:
            if node.val > query:
                node = node.left
            elif node.val == query:
                break
            else:
                node = node.right

        if node is None:
            # not found
            return

        if node.left is None and node.right is None:
            if node.attr == "left_child": node.parent.left = None
            else: node.parent.right = None

        elif node.right is None:
            # only left is None
            if node.attr == "left_child":
                node.parent.left = node.left
            else:
                node.parent.right = node.left
                node.left.attr = "right_child"

        elif node.left is None:
            # only right is None
            if node.attr == "left_child":
                node.parent.left = node.right
                node.right.attr = "left_child"
            else:
                node.parent.right  = node.right

        else:
            suc = self.getSuccessor(node)
            node.val = suc.val
            suc.parent.left = None

    def getSuccessor(self, node_):
        parent = None
        node = node_
        while node is not None:
            parent = node
            node = node.left

        return parent
    
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

    # tree.delete(12)
    # tree.view()
