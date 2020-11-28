import numpy as np
import math
from Node import Node


class FibHeap:
    def __init__(self):
        self.min = None
        self.n = 0

    def insert(self, x):
        x.degree = 0
        x.p = None
        x.child = None
        x.mark = False
        if self.min is None:
            self.min = x
        else:
            self.min.insert(x)
            if self.min.key > x.key:
                self.min = x

        self.n += 1

    @staticmethod
    def union(a, b):
        heap = FibHeap()
        heap.min = a.min
        heap.min = a.min.concat(b.min)
        if (a.min is None) or (b.min is not None and b.min.key < a.min.key):
            heap.min = b.min
        heap.n = a.n + b.n
        return heap

    def extractMin(self):
        z = self.min
        if z is not None:
            # have to store them in memory since the loop moves them
            if z.child is not None:
                children = [node for node in z.child.getSiblings()]
                for node in children:
                    z.insert(node)
                    node.p = None
            if z == self.min:
                self.min = z.right
            otherMin = z.right
            z.remove()
            if z == self.min:
                self.min = None
            else:
                self.min = otherMin
                self.consolidate()
            self.n -= 1
        return z

    def consolidate(self):
        distinct = np.empty(int(np.floor(FibHeap.D(self.n))), dtype=Node)
        rootlist = [node for node in self.min.getSiblings()]
        for w in rootlist:
            x = w
            d = x.degree
            while distinct[d] is not None:
                y = distinct[d]
                if x.key > y.key:
                    x, y = y, x
                self.link(y, x)
                distinct[d] = None
                d = d + 1
            distinct[d] = x
        self.min = None
        for degree, node in enumerate(distinct):
            if node is not None:
                if self.min is None:
                    self.min = node
                    node.left, node.right = node, node

                else:
                    self.min.insert(node)
                    if node.key < self.min.key:
                        self.min = node

    @staticmethod
    def D(x):
        goldenRatio = (1 + math.sqrt(5))/2
        return math.log(x, goldenRatio)

    def link(self, y, x):
        # make y a child of x, y must have smaller value than x
        if self.min == y:  # keep a pointer on the top layer
            self.min = x
        y.remove()
        if x.child is None:
            x.child = y
        else:
            x.child.insert(y)
        y.p = x
        x.degree += 1
        y.mark = False

    def decreaseKey(self, x, k):
        assert k < x.key
        x.key = k
        parent = x.p
        if parent is not None and x.key < parent.key:
            self.cut(x, parent)
            self.cascadingCut(parent)
        if x.key < self.min.key:
            self.min = x

    def cut(self, x, parent):
        # maybe check if x really in children?
        parent.degree -= 1
        x.remove()
        self.min.insert(x)
        x.p = None
        x.mark = False

    def cascadingCut(self, y):
        parent = y.p
        if parent is not None:
            if not y.mark:
                y.mark = True
            else:
                self.cut(y, parent)
                self.cascadingCut(parent)

    def delete(self, x):
        # assumes no other key is -infinity
        self.decreaseKey(x, -math.inf)
        self.extractMin()

    @staticmethod
    def validate(top):
        """
        a forest is valid if
        np.all(np.array([validate(tree) for tree in min.getSiblngs()]))
        """
        print(top.key)
        if top.child is None or top is None:
            return True
        print([node.key for node in top.child.getSiblings()])
        if top.key > min(node.key for node in top.child.getSiblings()):
            return False
        return all(FibHeap.validate(node) for node in top.child.getSiblings())


if __name__ == '__main__':
    dll = DLL()
    # dll.insert(Node(3))
    # dll.insert(Node(5))
    # dll.insert(Node(6))
    nodes = dll.getLayerList(Node(3))
    #print(next(nodes))
    for node in nodes:
        print(node.key)
