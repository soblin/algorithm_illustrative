# -*- coding: utf-8 -*-
import sys
input = sys.stdin.readline
from enum import Enum
import warnings
import graphviz
from collections import deque
import random

class Color(Enum):
    RED = 0
    BLACK = 1

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.color = None
        self.viz_id = 0

    def is_left(self):
        return self.val < self.parent.val

    def is_right(self):
        return not self.is_left()

    def is_leaf(self):
        return self.left is None and self.right is None

    def sibling(self):
        if self.is_left():
            return self.parent.right
        else:
            return self.parent.left

    def uncle(self):
        return self.parent.sibling()
    
class PureBinaryTree(object):
    def __init__(self):
        self.root = None

    def is_root(self, node):
        return node is self.root

    def insert(self, x):
        if not hasattr(self, "_insert"):
            raise NotImplementedError("insert cannot be called")

        return self._insert(x)

    def view(self):
        if not hasattr(self, "_view"):
            raise NotImplementedError("insert cannot be called")

        return self._view()

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
    
    def get_successor(self, node_):
        parent = None
        node = node_.right
        while node is not None:
            parent = node
            node = node.left

        return parent

    def rotate_right(self, node):
        if node is None:
            warnings.warn("cannot rotate_right None")
            return
        if node.left is None:
            warnings.warn("cannot rotate_right if node.left is None")
            return

        parent = node.parent
        lnode = node.left
        lrnode = lnode.right
        if node.parent is not None:
            is_left = node.is_left()
        #1
        node.left = lrnode
        if lrnode:
            lrnode.parent = node
        #2
        lnode.right = node
        node.parent = lnode
        if node is self.root:
            self.root = lnode
            self.root.parent = None
            return self.root
        
        if is_left:
            lnode.parent = parent
            parent.left = lnode
            return lnode
        else:
            lnode.parent = parent
            parent.right = lnode
            return lnode

    def rotate_left(self, node):
        if node is None:
            warnings.warn("cannot rotate_left None")
            return
        if node.right is None:
            warnings.warn("cannot rotate_left if node.right is None")
            return

        parent = node.parent
        rnode = node.right
        rlnode = rnode.left
        if node.parent is not None:
            is_left = node.is_left()
        #1
        node.right = rlnode
        if rlnode:
            rlnode.parent = node
        #2
        rnode.left = node
        node.parent = rnode
        if node is self.root:
            self.root = rnode
            self.root.parent = None
            return self.root
        
        if is_left:
            rnode.parent = parent
            parent.left  = rnode
            return rnode
        else:
            rnode.parent = parent
            parent.right = rnode
            return rnode

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
        node = self.find(query)

        if node is None:
            return

        if node.left is None and node.right is None:
            # no children
            if self.is_root(node): self.root = None
            elif node.is_left(): node.parent.left = None
            else: node.parent.right = None

        elif node.right is None:
            # only left child
            if self.is_root(node):
                self.root = node.left
                self.root.parent = None
            elif node.is_left():
                node.parent.left = node.left
                node.left.parent = node.parent
            else:
                node.parent.right = node.left
                node.left.parent = node.parent
        elif node.left is None:
            # only right child
            if self.is_root(node):
                self.root = node.right
                self.root.parent = None
            elif node.is_left():
                node.parent.left = node.right
                node.right.parent = node.parent
            else:
                node.parent.right  = node.right
                node.right.parent = node.parent
        else:
            # two children
            suc = self.get_successor(node)
            if suc is node.right:
                node.val = suc.val
                node.right = suc.right
                if suc.right:
                    node.right.parent = node
            else:
                node.val = suc.val
                suc.parent.left = suc.right
                if suc.parent.left:
                    suc.parent.left.parent = suc.parent

    def _view(self):
        g = graphviz.Digraph()
        queue = deque()
        viz_index = 0
        self.root.viz_id = viz_index
        queue.append(self.root)
        # BFS
        while len(queue) is not 0:
            node = queue.pop()
            # visualize node
            if node.is_leaf():
                g.node(str(node.viz_id), label="{0}".format(node.val), shape='square')
            else:
                if self.is_root(node):
                    g.node(str(node.viz_id), label="{0}".format(node.val), shape="triangle")
                else:
                    g.node(str(node.viz_id), label="{0}".format(node.val))

            # add edge
            if node.left is not None:
                viz_index += 1
                node.left.viz_id = viz_index
                queue.append(node.left)
                g.edge(str(node.viz_id), str(node.left.viz_id), label=str(node.val))
                # add empty for better visualization
                if node.right is None:
                    viz_index += 1
                    g.node(str(viz_index), shape="point")
                    g.edge(str(node.viz_id), str(viz_index), style="dashed")
                    
            if node.right is not None:
                # add empty for better visualization
                if node.left is None:
                    viz_index += 1
                    g.node(str(viz_index), shape="point")
                    g.edge(str(node.viz_id), str(viz_index), style="dashed")
                
                viz_index += 1
                node.right.viz_id = viz_index
                queue.append(node.right)
                g.edge(str(node.viz_id), str(node.right.viz_id), label=str(node.val))
        
        g.view()

class RBTree(PureBinaryTree):
    def __init__(self):
        super().__init__()
        self.g = None
        
    def is_black(self, node):
        if node is None:
            return True
        else:
            return node.color is Color.BLACK

    def is_red(self, node):
        return node.color is Color.RED
    
    def _insert(self, x):
        if self.root is None:
            self.root = Node(x)
            self.root.color = Color.BLACK
            return
        
        node = self.root
        parent = None
        while node is not None:
            parent = node
            if x < node.val:
                node = node.left
            else:
                node = node.right

        new_node = Node(x)
        new_node.color = Color.RED
        if x < parent.val:
            parent.left = new_node
            new_node.parent = parent
        else:
            parent.right = new_node
            new_node.parent = parent

        self.rebalance_insert(new_node)

    def rebalance_insert(self, node):
        if node is None:
            return
        if node is self.root:
            self.root.color = Color.BLACK
            return
        
        assert(self.is_red(node))
        
        if self.is_black(node.parent):
            return

        # node.parent.is_red()
        elif self.is_black(node.uncle()):
            # LL case
            if node.is_left() and node.parent.is_left():
                top = self.rotate_right(node.parent.parent)
                self.update_color(top)
                return
            if node.is_right() and node.parent.is_left():
                tmp = self.rotate_left(node.parent)
                top = self.rotate_right(tmp.parent)
                self.update_color(top)
                return
            if node.is_right() and node.parent.is_right():
                top = self.rotate_left(node.parent.parent)
                self.update_color(top)
                return
            if node.is_left() and node.parent.is_right():
                tmp = self.rotate_right(node.parent)
                top = self.rotate_left(tmp.parent)
                self.update_color(top)
                return
            
        elif self.is_red(node.uncle()):
            node.parent.color = Color.BLACK
            node.uncle().color = Color.BLACK
            node.parent.parent.color = Color.RED
            self.rebalance_insert(node.parent.parent)
            return
    
    def update_color(self, top):
        top.color = Color.BLACK
        if top.left:
            top.left.color = Color.RED
        if top.right:
            top.right.color = Color.RED

    def vis_node(self, node, shape):
        if node.color is Color.BLACK:
            self.g.node(str(node.viz_id), label="{0}".format(node.val), shape=shape, fillcolor='gray72', style="filled")
        else:
            self.g.node(str(node.viz_id), label="{0}".format(node.val), shape=shape, fillcolor='#fb9a99', style="filled")
    def _view(self):
        self.g = graphviz.Digraph()
        queue = deque()
        viz_index = 0
        self.root.viz_id = viz_index
        queue.append(self.root)
        # BFS
        while len(queue) is not 0:
            node = queue.popleft()
            # visualize node
            if node.is_leaf():
                self.vis_node(node, "square")
            else:
                if self.is_root(node):
                    self.vis_node(node, "triangle")
                else:
                    self.vis_node(node, "circle")

            # add edge
            if node.left is not None:
                viz_index += 1
                node.left.viz_id = viz_index
                queue.append(node.left)
                self.g.edge(str(node.viz_id), str(node.left.viz_id), label=str(node.val))
                # add empty for better visualization
                if node.right is None:
                    viz_index += 1
                    self.g.node(str(viz_index), shape="point")
                    self.g.edge(str(node.viz_id), str(viz_index), style="dashed")
                    
            if node.right is not None:
                # add empty for better visualization
                if node.left is None:
                    viz_index += 1
                    self.g.node(str(viz_index), shape="point")
                    self.g.edge(str(node.viz_id), str(viz_index), style="dashed")
                
                viz_index += 1
                node.right.viz_id = viz_index
                queue.append(node.right)
                self.g.edge(str(node.viz_id), str(node.right.viz_id), label=str(node.val))
        
        self.g.view()


if __name__ == '__main__':
    tree = RBTree()
    values = random.sample(range(200), 100)
    for val in values:
        tree.insert(val)

    print("type 'insert x' or 'delete x' or 'rotateR x' 'rotateL x' or 'view'. type q to quit.")

    while True:
        inputs = list(input().split())
        if len(inputs) == 1:
            cmd = str(inputs[0])
            if cmd == 'q':
                exit()
            elif cmd == "view":
                tree.view()
            else:
                print("type 'q' or 'view'")
        elif len(inputs) == 2:
            cmd = str(inputs[0])
            x = int(inputs[1])
            if cmd == "insert":
                tree.insert(x)
            elif cmd == "delete":
                tree.delete(x)
            elif cmd == "rotateR":
                tree.rotateR(tree.find(x))
            elif cmd == "rotateL":
                tree.rotateL(tree.find(x))
            else:
                print("type 'insert x' or 'rotateR x' or 'rotateL x")

