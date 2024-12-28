from __future__ import annotations
from typing import Tuple

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def to_tuple(self) -> Tuple:
        return self.x, self.y

    def __lt__(self, other: Point) -> bool:
        return self.x < other.x

    def __gt__(self, other: Point) -> bool:
        return self.x > other.x

    def is_left(self, q: Point) -> bool:
        return self < q

    @staticmethod
    def cross_product(p: Point, q: Point, r: Point) -> float:
        return (q.x - p.x) * (r.y - q.y) - (q.y - p.y) * (r.x - q.x)

class Segment:
    eps = 10 ** -16

    def __init__(self, p: Point, q: Point):
        if p.x < q.x:
            self.left = p
            self.right = q
        else:
            self.left = q
            self.right = p

        self.a = (self.left.y - self.right.y) / (self.left.x - self.right.x)
        self.b = self.right.y - self.right.x * self.a

    def __repr__(self) -> str:
        return f"[{self.left}, {self.right}]"

    def position(self, q: Point) -> int:
        cross_product = Point.cross_product(self.left, self.right, q)
        if cross_product < -Segment.eps:
            return 1
        elif cross_product > Segment.eps:
            return -1
        return 0

    def to_tuple(self):
        return (self.left.x, self.left.y), (self.right.x, self.right.y)

class Trapezoid:
    def __init__(self, left: Point, right: Point, up: Segment, down: Segment):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

        self.top_left = None
        self.bottom_left = None
        self.top_right = None
        self.bottom_right = None

        self.leaf = None

    def __repr__(self) -> str:
        return f"[{self.left}, {self.right}, {self.up}, {self.down}]"

class Leaf:
    def __init__(self, trapezoid):
        self.trapezoid = trapezoid

    def __repr__(self) -> str:
        return f"{self.trapezoid}"

class Node:
    def __init__(self):
        self.left = None
        self.right = None

    @staticmethod
    def is_x_node(node: (Node, Leaf)) -> bool:
        return isinstance(node, XNode)

    @staticmethod
    def is_y_node(node: (Node, Leaf)) -> bool:
        return isinstance(node, YNode)

    @staticmethod
    def is_leaf(node: (Node, Leaf)) -> bool:
        return isinstance(node, Leaf)

class XNode(Node):
    def __init__(self, p: Point):
        super().__init__()
        self.p = p

class YNode(Node):
    def __init__(self, s: Segment):
        super().__init__()
        self.s = s

class DTree:
    def __init__(self):
        self.root = None

#   TODO: Dlaczego a nie jest nigdy aktualizowane?
    def find(self, node: (Node, YNode, XNode), point: Point, a: float = None):
        if Node.is_leaf(node):
            return node.trapezoid
        elif Node.is_x_node(node):
            if node.p > point:
                return self.find(node.left, point, a)
            else:
                return self.find(node.right, point, a)
        else:
            position = node.s.position(point)
            if position == 1:
                return self.find(node.right, point, a)
            elif position == 0:
                if node.s.a < a:
                    return self.find(node.left, point, a)
                else:
                    return self.find(node.right, point, a)
            else:
                self.find(node.right, point, a)
