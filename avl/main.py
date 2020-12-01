# -*- coding: utf-8 -*-
import graphviz
from collections import deque

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.viz_id = None

class PureBinaryTree(object):
    def __init__(self):
        self.root = None

    def isLeaf(self, node):
        return node.left is None and node.right is None

    def isRoot(self, node):
        return node.parent is None

    def isLeft(self, node):
        parent = node.parent
        if parent is None:
            return None
        if node.val <= parent.val:
            return True
        else:
            return False
    
    def insert(self, x):
        if not hasattr(self, "_insert"):
            raise NotImplementedError("insert cannot be called")

        return self._insert(x)

    def delete(self, x):
        if not hasattr(self, "_delete"):
            raise NotImplementedError("delete cannot be called")

        return self._delete(x)

    def find(self, x):
        node = self.root
        while node is not None:
            if node.val == x:
                return node
            if x <= node.val:
                node = node.left
            else:
                node = node.right

        return None
    
    def getSuccessor(self, node_):
        parent = None
        node = node_
        while node is not None:
            parent = node
            node = node.left

        return parent

    def rotateR(self, node):
        if node is None:
            raise IndexError("rotateR must not be used for None node")
        if node.left is None or node.right is None:
            raise IndexError("node.left and node.right must not be None")
        
        parent = node.parent
        lnode = node.left
        lrnode = lnode.right
        is_left = self.isLeft(node)
        # 1
        node.left = lrnode
        if lrnode:
            lrnode.parent = node
        # 2
        lnode.right = node
        node.parent = lnode

        if node is self.root:
            # 3
            self.root = lnode
            self.root.parent = None
        
        elif is_left:
            # 3
            lnode.parent = parent
            parent.left = lnode
        
        else:
            # 3
            lnode.parent = parent
            parent.right = lnode
    
    def view(self):
        g = graphviz.Graph()
        queue = deque()
        viz_index = 0
        self.root.viz_id = viz_index
        queue.append(self.root)
        # BFS
        while len(queue) is not 0:
            node = queue.pop()
            # visualize node
            if self.isLeaf(node):
                g.node(str(node.viz_id), label="{0}({1})".format(node.val, node.parent.val), shape='square')
            else:
                if not self.isRoot(node):
                    g.node(str(node.viz_id), label="{0}({1})".format(node.val, node.parent.val))
                else:
                    g.node(str(node.viz_id), label="{0}".format(node.val))

            # add edge
            if node.left is not None:
                viz_index += 1
                node.left.viz_id = viz_index
                queue.append(node.left)
                g.edge(str(node.viz_id), str(node.left.viz_id))
                # add empty for better visualization
                if node.right is None:
                    viz_index += 1
                    g.node(str(viz_index), shape="point")
                    g.edge(str(node.viz_id), str(viz_index))
                    
            if node.right is not None:
                # add empty for better visualization
                if node.left is None:
                    viz_index += 1
                    g.node(str(viz_index), shape="point")
                    g.edge(str(node.viz_id), str(viz_index))
                
                viz_index += 1
                node.right.viz_id = viz_index
                queue.append(node.right)
                g.edge(str(node.viz_id), str(node.right.viz_id))
        
        g.view()

class BinaryTree(PureBinaryTree):
    def __init__(self):
        super().__init__()
 
    def _insert(self, x):
        if self.root is None:
            self.root = Node(x)
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
            parent.left = node
        else:
            node = Node(x)
            node.parent = parent
            parent.right = node

        return

    def _delete(self, query):
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
            if self.isLeft(node): node.parent.left = None
            else: node.parent.right = None

        elif node.right is None:
            # only left is None
            if self.isLeft(node):
                node.parent.left = node.left
            else:
                node.parent.right = node.left

        elif node.left is None:
            # only right is None
            if self.isLeft(node):
                node.parent.left = node.right
            else:
                node.parent.right  = node.right

        else:
            suc = self.getSuccessor(node)
            node.val = suc.val
            suc.parent.left = None

class AVLTree(PureBinaryTree):
    def __init__(self):
        super().__init__()
 
    def _insert(self, x):
        pass

if __name__ == '__main__':
    tree = BinaryTree()
    values = [7, 10, 13, 5, 3, 6, 1, 4, 17, 25, 12]
    for val in values:
        tree.insert(val)
    
    # tree.delete(12)
    tree.view()
