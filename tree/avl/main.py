# -*- coding: utf-8 -*-
import graphviz
from collections import deque
import warnings
import sys
input = sys.stdin.readline

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.viz_id = None
        self.balance = 0

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
    
    def getSuccessor(self, node_):
        parent = None
        node = node_.right
        while node is not None:
            parent = node
            node = node.left

        return parent

    def rotateR(self, node):
        if node is None:
            warnings.warn("rotateR applied for None. Ignore")
            return
        if node.left is None:
            warnings.warn("rotateR applied with left node None. Ignore")
            return
        
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
            self.root = lnode
            self.root.parent = None
            return self.root
        
        elif is_left:
            lnode.parent = parent
            parent.left = lnode
            return lnode
        
        else:
            lnode.parent = parent
            parent.right = lnode
            return lnode
        
    def rotateL(self, node):
        if node is None:
            warnings.warn("rotateR applied for None. Ignore")
            return
        if node.right is None:
            warnings.warn("rotateR applied with right node None. Ignore")
            return
        
        parent = node.parent
        rnode = node.right
        rlnode = rnode.left
        is_left = self.isLeft(node)
        # 1
        node.right = rlnode
        if rlnode:
            rlnode.parent = node
        # 2
        rnode.left = node
        node.parent = rnode

        if node is self.root:
            self.root = rnode
            self.root.parent = None
            return self.root
        
        elif is_left:
            rnode.parent = parent
            parent.left = rnode
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
            # not found
            return

        if node.left is None and node.right is None:
            if self.isRoot(node): self.root = None
            elif self.isLeft(node): node.parent.left = None
            else: node.parent.right = None

        elif node.right is None:
            # only left child
            if self.isRoot(node):
                self.root = node.left
                self.root.parent = None
            elif self.isLeft(node):
                node.parent.left = node.left
                node.left.parent = node.parent
            else:
                node.parent.right = node.left
                node.left.parent = node.parent
        elif node.left is None:
            # only right child
            if self.isRoot(node):
                self.root = node.right
                self.root.parent = None
            elif self.isLeft(node):
                node.parent.left = node.right
                node.right.parent = node.parent
            else:
                node.parent.right  = node.right
                node.right.parent = node.parent
        else:
            suc = self.getSuccessor(node)
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
            if self.isLeaf(node):
                g.node(str(node.viz_id), label="{0}".format(node.val), shape='square')
            else:
                if self.isRoot(node):
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

class AVLTree(PureBinaryTree):
    def __init__(self):
        super().__init__()
 
    def _insert(self, x):
        pass

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

        node = Node(x)
        if x <= parent.val:
            node.parent = parent
            parent.left = node
        else:
            node.parent = parent
            parent.right = node

        self.rebalanceInsert(node)

    def rebalanceInsert(self, new_node):
        node = new_node
        while node.parent is not None:
            pnode = node.parent
            if self.isLeft(node):
                pnode.balance += 1
            else:
                pnode.balance -= 1

            if pnode.balance is 0:
                return

            if pnode.balance == 2:
                if pnode.left.balance == -1:
                    # LR
                    pnode.left = self.rotateL(pnode.left)
                    node = self.rotateR(pnode)
                    self.updateBalance(node)
                elif pnode.left.balance == 1:
                    # LL
                    node = self.rotateR(pnode)
                    node.balance = 0
                    node.right.balance = 0
                break
            elif pnode.balance == -2:
                if pnode.right.balance == -1:
                    # RR
                    node = self.rotateL(pnode)
                    node.balance = 0
                    node.left.balance = 0
                elif pnode.right.balance == 1:
                    # RL
                    pnode.right = self.rotateR(pnode.left)
                    node = self.rotateL(pnode)
                    self.updateBalance(node)
                break

            node = pnode

    def updateBalance(self, node):
        if node.balance == 1:
            node.left.balance = 0
            node.right.balance = -1
        elif node.balance == -1:
            node.left.balance = 1
            node.right.balance = 0
        else:
            node.left.balance = 0
            node.right.balance = 0
        
        node.balance = 0

    def _delete(self, query):
        to_remove = self.find(query)

        if to_remove is None:
            return

        to_balance = None
        if to_remove.left is not None and to_remove.right is not None:
            # two children
            suc = self.getSuccessor(to_remove)
            to_remove.val = suc.val
            if suc is to_remove.right:
                to_remove.val = suc.val
                to_remove.right = suc.right
                if suc.right:
                    to_remove.right.parent = to_remove
                to_balance = to_remove.right
            else:
                suc.parent.left = suc.right
                if suc.parent.left:
                    suc.parent.left.parent = suc.parent
                to_balance = suc
        elif to_remove.left is not None:
            # only left
            if self.isRoot(to_remove):
                self.root = to_remove.left
                self.root.parent = None
                return
            elif self.isLeft(to_remove):
                to_remove.parent.left = to_remove.left
                to_remove.left.parent = to_remove.parent
                to_balance = to_remove.left
            else:
                to_remove.parent.right = to_remove.left
                to_remove.left.parent = to_remove.parent
                to_balance = to_remove.left
        elif to_remove.right is not None:
            # only right
            if self.isRoot(to_remove):
                self.root = to_remove.right
                self.root.parent = None
                return
            elif self.isLeft(to_remove):
                to_remove.parent.left = to_remove.right
                to_remove.right.parent = to_remove.parent
                to_balance = to_remove.right
            else:
                to_remove.parent.right = to_remove.right
                to_remove.right.parent = to_remove.parent
                to_balance = to_remove.right
        else:
            if self.isRoot(to_remove):
                self.root = None
                return
            elif self.isLeft(to_remove):
                to_remove.parent.left = None
                to_balance = to_remove
            else:
                to_remove.parent.right = None
                to_balance = to_remove
                
        self.rebalanceDelete(to_balance)

    def rebalanceDelete(self, removed):
        node = removed
        while node.parent is not None:
            pnode = node.parent
            if self.isLeft(node):
                pnode.balance -= 1
            else:
                pnode.balance += 1

            if pnode.balance is 1 or pnode.balance is -1:
                return

            if pnode.balance is -2:
                if pnode.right.balance is 0:
                    top = self.rotateL(pnode)
                    top.balance = 1
                    top.left.balance = -1
                elif pnode.right.balance is -1:
                    top = self.rotateL(pnode)
                    top.balance = 0
                    top.left.balance = 0
                elif pnode.right.balance is 1:
                    pnode.right = self.rotateR(pnode.right)
                    top = self.rotateL(pnode)
                    self.updateBalance(top)
                if top.balance != 0:
                    break
                else:
                    node = top
                    
            if pnode.balance is 2:
                if pnode.left.balance is 0:
                    top = self.rotateR(pnode)
                    top.balance = -1
                    top.right.balance = 1
                elif pnode.left.balance is 1:
                    top = self.rotateR(pnode)
                    top.balance = 0
                    top.right.balance = 0
                elif pnode.left.balance is -1:
                    pnode.left = self.rotateL(pnode.left)
                    top = self.rotateR(pnode)
                    self.updateBalance(top)
                if top.balance != 0:
                    break
                else:
                    node = top
            else:
                node = pnode

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
            if self.isLeaf(node):
                g.node(str(node.viz_id), label="{0}[{1}]".format(node.val, node.balance), shape='square')
            else:
                if self.isRoot(node):
                    g.node(str(node.viz_id), label="{0}[{1}]".format(node.val, node.balance), shape="triangle")
                else:
                    g.node(str(node.viz_id), label="{0}[{1}]".format(node.val, node.balance))

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

if __name__ == '__main__':
    # tree = BinaryTree()
    tree = AVLTree()
    values = [7, 10, 13, 5, 3, 6, 1, 4, 17, 25, 12, 15, 20, 30, 40]
    for val in values:
        tree.insert(val)
    
    # tree.delete(12)
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
    
    
