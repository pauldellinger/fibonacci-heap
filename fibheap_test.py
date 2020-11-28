from FibHeap import FibHeap
from Node import Node
from random import shuffle, choice
import numpy as np


def test_heap_make():
    heap = FibHeap()
    assert heap.min is None
    assert heap.min is None
    assert heap.n == 0


def test_heap_add_one():
    heap = FibHeap()
    x = Node(0)
    heap.insert(x)
    assert heap.n == 1
    assert heap.min == x
    assert heap.min.p is None and heap.min.child is None
    assert not heap.min.mark
    assert x in heap.min.getSiblings()


def test_heap_add_many():
    # should add them all in min list until consolidation
    heap = FibHeap()
    nodes = [Node(x) for x in range(100)]
    shuffle(nodes)  # shuffle for good measure
    for node in nodes:
        heap.insert(node)
    assert heap.min.key == 0
    for node in nodes:
        assert node in heap.min.getSiblings()
    assert heap.n == 100


def test_heap_link_simple():
    heap = FibHeap()
    a = Node(0)
    b = Node(1)
    heap.insert(a)
    heap.insert(b)
    assert heap.min == a
    heap.link(b, a)  # b should be child of a
    assert b not in a.getSiblings()
    assert b == a.child
    assert heap.min == a
    assert a.degree == 1


def test_heap_link_3():
    heap = FibHeap()
    a, b, c = Node(0), Node(1), Node(2)
    for node in a, b, c:
        heap.insert(node)
    heap.link(c, b)
    heap.link(b, a)
    assert a.child.child == c
    assert a.degree == 1 and b.degree == 1 and c.degree == 0
    assert c.p.p == a
    nodes = set([a, b, c])
    for node in nodes:
        assert node.left == node and node.right == node
        for other in nodes - set([node]):
            # make sure every node by itself
            assert node not in other.getSiblings()
    assert heap.min == a


def test_heap_validate_simple():
    heap = FibHeap()
    nodes = [Node(x) for x in range(10)]
    for node in nodes:
        heap.insert(node)
    # all in min list now
    assert all(FibHeap.validate(tree) for tree in heap.min.getSiblings())


def test_heap_invalid_simple():
    heap = FibHeap()
    nodes = [Node(x) for x in range(10)]
    for node in nodes:
        heap.insert(node)
    heap.link(nodes[4], nodes[9])
    # should fail now because 10 is now parent of 5
    # all in min list now
    assert not all(FibHeap.validate(tree) for tree in heap.min.getSiblings())


def test_heap_valid_complex():
    heap = FibHeap()
    nodes = [Node(x) for x in range(10)]
    for node in nodes:
        heap.insert(node)
    # make a more complicated tree structure
    for node in (nodes[1], nodes[2], nodes[3]):
        heap.link(node, nodes[0])
    for node in (nodes[4], nodes[5]):
        heap.link(node, nodes[2])
    heap.link(nodes[6], nodes[4])
    for node in (nodes[7], nodes[8]):
        heap.link(node, nodes[5])

    """
        0       9
     /  |  \
     1  2   3
       / \
      4   5
     /   / \
    6   7   8

    """
    assert all(FibHeap.validate(tree) for tree in heap.min.getSiblings())
    assert heap.min.key == 0


def test_heap_invalid_complex():
    heap = FibHeap()
    nodes = [Node(x) for x in range(10)]
    for node in nodes:
        heap.insert(node)
    # make a more complicated tree structure
    for node in (nodes[1], nodes[4], nodes[5]):
        heap.link(node, nodes[0])
    for node in (nodes[2], nodes[3]):
        heap.link(node, nodes[4])
    heap.link(nodes[6], nodes[2])
    for node in (nodes[7], nodes[8]):
        heap.link(node, nodes[3])

    """
        0       9
     /  |  \
     1  4   5
       / \
      2   3
     /   / \
    6   7   8

    """
    assert not all(FibHeap.validate(tree) for tree in heap.min.getSiblings())
    assert heap.min.key == 0


def construct_textbook_ex():
    # example from Intro to Algorithms, 3rd edition, Chapter 19
    keys = [23, 7, 21, 3, 17, 24, 18,
            52, 38, 30, 26, 46, 39, 41, 35]
    d = {}
    heap = FibHeap()
    for key in keys:
        node = Node(key)
        d[str(key)] = node
        heap.insert(node)
    heap.link(d['39'], d['18'])
    heap.link(d['41'], d['38'])
    heap.link(d['35'], d['26'])
    heap.link(d['18'], d['3'])
    heap.link(d['52'], d['3'])
    heap.link(d['38'], d['3'])
    heap.link(d['30'], d['17'])
    heap.link(d['26'], d['24'])
    heap.link(d['46'], d['24'])
    for node in ('18', '39', '26'):
        d[node].mark = True
    return heap


def test_extract_min():
    example = construct_textbook_ex()
    min = example.extractMin()
    assert min.key == 3
    assert example.min.key == 7
    assert example.n == 14
    assert all(FibHeap.validate(tree) for tree in example.min.getSiblings())


def test_heap_extract_many():
    heap = FibHeap()
    nodes = [Node(x) for x in range(500)]
    for node in nodes:
        heap.insert(node)
    for x in range(500):
        min = heap.extractMin()
        assert min.key == x
        assert heap.n == 499 - x
        print(heap.min)
        if x < 499:
            assert all(FibHeap.validate(tree) for tree in heap.min.getSiblings())
        else:
            assert heap.min is None


def test_heap_cut():
    heap = FibHeap()
    nodes = [Node(x) for x in range(10)]
    for node in nodes:
        heap.insert(node)
    # make a more complicated tree structure
    for node in (nodes[1], nodes[2], nodes[3]):
        heap.link(node, nodes[0])
    for node in (nodes[4], nodes[5]):
        heap.link(node, nodes[2])
    heap.link(nodes[6], nodes[4])
    for node in (nodes[7], nodes[8]):
        heap.link(node, nodes[5])

    """
        0       9
     /  |  \
     1  2   3
       / \
      4   5
     /   / \
    6   7   8

    """
    degree = nodes[2].degree
    heap.cut(nodes[5], nodes[2])
    assert degree - 1 == nodes[2].degree
    assert nodes[5] in heap.min.getSiblings()
    assert nodes[7] in nodes[5].child.getSiblings()
    assert nodes[8] in nodes[5].child.getSiblings()
    assert nodes[5] not in nodes[2].child.getSiblings()
    assert nodes[5].p is None and nodes[5].mark is False


def test_heap_cascading_cut_textbook():
    # construct the textbook example again
    keys = [23, 7, 21, 3, 17, 24, 18,
            52, 38, 30, 26, 46, 39, 41, 35]
    d = {}
    heap = FibHeap()
    for key in keys:
        node = Node(key)
        d[str(key)] = node
        heap.insert(node)
    heap.link(d['39'], d['18'])
    heap.link(d['41'], d['38'])
    heap.link(d['35'], d['26'])
    heap.link(d['18'], d['3'])
    heap.link(d['52'], d['3'])
    heap.link(d['38'], d['3'])
    heap.link(d['30'], d['17'])
    heap.link(d['26'], d['24'])
    heap.link(d['46'], d['24'])
    for node in ('18', '39', '26'):
        d[node].mark = True
    heap.extractMin()

    heap.decreaseKey(d['46'], 15)

    assert(FibHeap.validate(tree) for tree in heap.min.getSiblings())
    assert d['18'].mark
    assert d['39'].mark
    assert d['24'].mark
    assert d['46'] in heap.min.getSiblings()

    heap.decreaseKey(d['35'], 5)
    assert not d['26'].mark
    assert not d['24'].mark
    for node in ('46', '35', '26', '24'):
        assert d[node] in heap.min.getSiblings()
    assert heap.min.key == 5


if __name__ == '__main__':
    example = construct_textbook_ex()
    min = example.extractMin()
    assert min.key == 3
    assert example.min.key == 7
    assert example.n == 14
    assert all(FibHeap.validate(tree) for tree in example.min.getSiblings())
