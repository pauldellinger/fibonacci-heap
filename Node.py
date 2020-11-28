class Node:
    def __init__(self,
                 key=None,
                 degree=0,
                 p=None,
                 child=None,
                 mark=False,
                 left=None,
                 right=None):
        self.key = key
        self.degree = degree
        self.p = p
        self.child = child
        self.mark = mark
        self.left = left if left is not None else self
        self.right = right if right is not None else self

    def insert(self, other):
        other.left = self.left
        other.right = self

        self.left.right = other
        self.left = other

    def remove(self):
        self.left.right = self.right
        self.right.left = self.left
        self.right = self
        self.left = self
        self.p = None
        #  it should get garbage collected now... right?!

    def concat(self, other):
        if other is None:
            return self
        # had to draw this one out
        other.left.right = self.right
        self.right.left = other.left
        self.right = other
        other.left = self
        return self

    def getSiblings(self):
        #  Use a genertor so we never store the whole list in memory
        yield self
        curr = self.right
        while curr != self:
            yield curr
            curr = curr.right
