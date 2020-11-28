from Node import Node


def test_node_create_empty():
    x = Node()
    assert x.key is None
    assert x.left == x
    assert x.right == x


def test_node_create():
    x = Node(3)
    assert x.key == 3
    assert x.left == x
    assert x.right == x


def test_node_insert():
    x = Node(3)
    y = Node(5)
    x.insert(y)
    assert x.left == y
    assert x.right == y
    assert y.left == x
    assert y.right == x


def test_node_insert_many():
    x = Node(100)
    for n in range(0, 100):
        y = Node(n)
        # inserts y to the left of x
        x.insert(y)
    y = x.right

    for n in range(101):
        assert y.key == n
        y = y.right


def test_node_remove():
    x, y, z = (Node(n) for n in range(3))
    x.insert(y)
    x.insert(z)

    # make sure we have a circle
    assert x.left == z
    assert x.right == y
    assert y.right == z
    assert y.left == x
    assert z.left == y
    assert z.right == x

    x.remove()
    # x should point to itself now
    assert x.left == x
    assert x.right == x

    assert y.right == z
    assert y.left == z

    assert z.right == y
    assert z.left == y


def test_node_concat():
    x = Node(10)
    for n in range(0, 10):
        node = Node(n)
        x.insert(node)
        # <- 0 <-> 1 <-> 2 ... 10 ->
    y = Node(-1)
    for n in range(9):
        node = Node(-2 - n)
        y.insert(node)
        # <- -10 <-> -9 <-> ...-1 ->

    x.concat(y)
    seen = set()
    for _ in range(20):
        seen.add(x.key)
        x = x.right
    assert len(seen) == 20


def test_node_getSiblings_count():
    x = Node(10)
    for n in range(10):
        node = Node(n)
        x.insert(node)
    siblings = x.getSiblings()
    count = 0
    for _ in siblings:
        count += 1
    assert count == 11


def test_node_getSiblings_value():
    x = Node(10)
    for n in range(10):
        node = Node(n)
        x.insert(node)
    siblings = x.getSiblings()
    count = 0
    assert 10 == next(siblings).key
    for n in range(10):
        y = next(siblings)
        assert y.key == n
