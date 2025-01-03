from __future__ import annotations
from typing import Tuple
from .utils import Position

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

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

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

    def position(self, q: Point) -> Position:
        cross_product = Point.cross_product(self.left, self.right, q)
        if cross_product > Segment.eps:
            return Position.ABOVE
        elif cross_product < -Segment.eps:
            return Position.BELOW
        return Position.ON

    def to_tuple(self):
        return (self.left.x, self.left.y), (self.right.x, self.right.y)

    def get_points(self):
        return self.left, self.right

    def get_y_from_x(self, x):
        return self.a * x + self.b

    def __eq__(self, other: Segment) -> bool:
        return self.left == other.left and self.right == other.right

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

    def get_points(self, as_tuples = False) -> tuple:
        p1 = Point(self.left.x, self.down.get_y_from_x(self.left.x))
        p2 = Point(self.right.x, self.down.get_y_from_x(self.right.x))
        p3 = Point(self.right.x, self.up.get_y_from_x(self.right.x))
        p4 = Point(self.left.x, self.up.get_y_from_x(self.left.x))
        if not as_tuples:
            return p1, p2, p3, p4
        return p1.to_tuple(), p2.to_tuple(), p3.to_tuple(), p4.to_tuple()

    def get_segments(self, as_tuples = False) -> tuple:
        p = self.get_points(as_tuples)
        if not as_tuples:
            return Segment(p[0], p[1]), Segment(p[1], p[2]), Segment(p[2], p[3]), Segment(p[3], p[0])
        return (p[0], p[1]), (p[1], p[2]), (p[2], p[3]), (p[3], p[0])

    def connect_to_top_left(self, trapezoid: (Trapezoid, None)):
        self.top_left = trapezoid
        if trapezoid is not None:
            trapezoid.top_right = self

    def connect_to_top_right(self, trapezoid: (Trapezoid, None)):
        self.top_right = trapezoid
        if trapezoid is not None:
            trapezoid.top_left = self

    def connect_to_bottom_left(self, trapezoid: (Trapezoid, None)):
        self.bottom_left = trapezoid
        if trapezoid is not None:
            trapezoid.bottom_right = self

    def connect_to_bottom_right(self, trapezoid: (Trapezoid, None)):
        self.bottom_right = trapezoid
        if trapezoid is not None:
            trapezoid.bottom_left = self

    def __eq__(self, other: Trapezoid) -> bool:
        return self.up == other.up and self.down == other.down and self.left == other.left and self.right == other.right

    def __hash__(self):
        return id(self)

class Leaf:
    def __init__(self, trapezoid: Trapezoid):
        self.trapezoid = trapezoid

    def __repr__(self) -> str:
        return f"{self.trapezoid}"

    def __eq__(self, other: Leaf) -> bool:
        if Node.are_same_type(self, other):
            return self.trapezoid == other.trapezoid

        return False

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

    @staticmethod
    def are_same_type(first: Node, second: Node):
        if (Node.is_leaf(first) and Node.is_leaf(second)) or (Node.is_y_node(first) and Node.is_y_node(second)) or (Node.is_x_node(first) and Node.is_x_node(second)):
            return True

        return False

class XNode(Node):
    def __init__(self, p: Point):
        super().__init__()
        self.p = p

    def __eq__(self, other):
        if Node.are_same_type(self, other):
            return self.p == other.p

        return False

class YNode(Node):
    def __init__(self, s: Segment):
        super().__init__()
        self.s = s

    def __eq__(self, other):
        if Node.are_same_type(self, other):
            return self.s == other.s

        return False

class DTree:
    def __init__(self):
        self.root = None

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
            if position == Position.ABOVE:
                return self.find(node.left, point, a)
            elif position == Position.BELOW:
                return self.find(node.right, point, a)
            else:
                if node.s.a < a:
                    return self.find(node.left, point, a)
                else:
                    return self.find(node.right, point, a)

    def find_parent(self, node: Node, target_node: Leaf):
        if not node:
            return None

        if self.root == target_node:
            return self.root
        if Node.is_leaf(node):
            return None

        if node.right == target_node or node.left == target_node:
            return node

        return self.find_parent(node.right, target_node) or self.find_parent(node.left, target_node)

    def update_single(self, trapezoid: Trapezoid, segment: Segment, up: Trapezoid, down: Trapezoid, left: (Trapezoid, None), right: (Trapezoid, None)):
        node = self.find_parent(self.root, trapezoid.leaf)
        p, q = segment.get_points()

        segment_left_node = XNode(p)
        segment_right_node = XNode(q)
        segment_node = YNode(segment)

        if left and right:
            if node == self.root:
                self.root = segment_left_node
            elif node.left == trapezoid.leaf:
                node.left = segment_left_node
            else:
                node.right = segment_left_node

            segment_left_node.left = Leaf(left)
            segment_left_node.right = segment_right_node

            segment_right_node.left = segment_node
            segment_right_node.right = Leaf(right)

            segment_node.left = Leaf(up)
            segment_node.right = Leaf(down)

        elif left and not right:
            if node == self.root:
                self.root = segment_left_node
            elif node.left == trapezoid.leaf:
                node.left = segment_left_node
            else:
                node.right = segment_left_node

            segment_left_node.left = Leaf(left)
            segment_left_node.right = segment_node

            segment_node.left = Leaf(up)
            segment_node.right = Leaf(down)

        elif not left and right:
            if node == self.root:
                self.root = segment_right_node
            elif node.left == trapezoid.leaf:
                node.left = segment_right_node
            else:
                node.right = segment_right_node

            segment_right_node.left = segment_node
            segment_right_node.right = Leaf(right)

            segment_node.left = Leaf(up)
            segment_node.right = Leaf(down)

    def update_multiple(self, trapezoids: list[Trapezoid], segment: Segment, splitted_trapezoids: list[Tuple[Trapezoid, Trapezoid]]):
        n = len(splitted_trapezoids)

        for i in range(1, n):
            trapezoid = trapezoids[i]
            node = self.find_parent(self.root, trapezoid.leaf)
            segment_node = YNode(segment)

            if node.left == trapezoid.leaf:
                node.left = segment_node
            else:
                node.right = segment_node

            segment_node.left = splitted_trapezoids[0][i]
            segment_node.right = splitted_trapezoids[0][i]
