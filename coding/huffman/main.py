# -*- coding: utf-8 -*-
import sys
input = sys.stdin.readline
from queue import PriorityQueue as PQueue

class Node:
    def __init__(self, c, n):
        self.c = c
        self.num = n

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
        return f'{self.c}:{self.num}'
    
if __name__ == '__main__':
    n_char = int(input())
    nodes = []
    queue = PQueue()
    for _ in range(n_char):
        inputs = list(input().split())
        c = str(inputs[0])
        n = int(inputs[1])
        queue.put(Node(c, n))
    
    while queue.qsize() is not 0:
        node = queue.get()
        print(node)
