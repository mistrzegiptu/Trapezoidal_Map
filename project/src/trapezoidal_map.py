from .data_structures import *
from .visualizer.main import Visualizer
import random

class TrapezoidalMap:
    def __init__(self, S: list[tuple[tuple[float, float], tuple[float, float]]]):
        permuted_s = random.sample(S, len(S))
        self.segments = self.__create_segments(permuted_s)
        self.rect_bound = self.__create_rect_bound()
        self.tree = DTree()
        self.tree.root = Leaf(self.rect_bound)

    def build_trapezoidal_map(self):
        for i in range(len(self.segments)):
            intersected_trapezoids = self.follow_segment(self.segments[i])
            self.update_map(intersected_trapezoids, self.segments[i])

        return self.tree

    def follow_segment(self, s: Segment):
        p, q = s.get_points()
        intersected_trapezoids = []
        first_trapezoid = self.tree.find(self.tree.root, p, s.a)
        intersected_trapezoids.append(first_trapezoid)

        j = 0
        while intersected_trapezoids[j].right < q:
            if s.position(intersected_trapezoids[j].right) == Position.ABOVE:
                intersected_trapezoids.append(intersected_trapezoids[j].bottom_right)
            else:
                intersected_trapezoids.append(intersected_trapezoids[j].top_right)
            j += 1
        return intersected_trapezoids

    @staticmethod
    def get_left_trapezoid(trapezoid, top, bottom, s):
        p, q = s.get_points()
        top_left = trapezoid.top_left
        bottom_left = trapezoid.bottom_left
        upper_segment = trapezoid.up
        lower_segment = trapezoid.down

        left = Trapezoid(trapezoid.left, p, upper_segment, lower_segment)
        left.connect_to_top_left(top_left)
        left.connect_to_bottom_left(bottom_left)
        left.connect_to_top_right(top)
        left.connect_to_bottom_right(bottom)
        top.connect_to_top_left(left)
        bottom.connect_to_bottom_left(left)

        return left

    @staticmethod
    def get_right_trapezoid(trapezoid, top, bottom, s):
        p, q = s.get_points()
        top_right = trapezoid.top_right
        bottom_right = trapezoid.bottom_right
        upper_segment = trapezoid.up
        lower_segment = trapezoid.down

        right = Trapezoid(q, trapezoid.right, upper_segment, lower_segment)
        right.connect_to_top_right(top_right)
        right.connect_to_bottom_right(bottom_right)
        right.connect_to_top_left(top)
        right.connect_to_bottom_left(bottom)
        top.connect_to_top_right(right)
        bottom.connect_to_bottom_right(right)

        return right

    @staticmethod
    def divide_single_trapezoid(trapezoid: Trapezoid, s: Segment):
        p, q = s.get_points()
        upper_segment = trapezoid.up
        lower_segment = trapezoid.down

        top = Trapezoid(p, q, upper_segment, s)
        bottom = Trapezoid(p, q, s, lower_segment)

        left = TrapezoidalMap.get_left_trapezoid(trapezoid, top, bottom, s)
        right = TrapezoidalMap.get_right_trapezoid(trapezoid, top, bottom, s)

        return top, bottom, left, right

    @staticmethod
    def divide_leftmost_trapezoid(trapezoid: Trapezoid, s:Segment):
        p, _ = s.get_points()
        top_right = trapezoid.top_right
        bottom_right = trapezoid.bottom_right
        upper_segment = trapezoid.up
        lower_segment = trapezoid.down
        right_point = trapezoid.right

        top = Trapezoid(p, right_point, upper_segment, s)
        bottom = Trapezoid(p, right_point, s, lower_segment)

        top.connect_to_top_right(top_right)
        bottom.connect_to_bottom_right(bottom_right)

        left = TrapezoidalMap.get_left_trapezoid(trapezoid, top, bottom, s)

        return top, bottom, left

    @staticmethod
    def connect_or_merge_to_previous_trapezoids(trapezoid, top, bottom, top_prev, bottom_prev, s):
        top_right = trapezoid.top_right
        top_left = trapezoid.top_left
        bottom_left = trapezoid.bottom_left
        bottom_right = trapezoid.bottom_right
        left_point = trapezoid.left

        if top_prev.up is top.up and top_prev.down is top.down:
            top = Trapezoid(top_prev.left, top.right, top.up, top.down)
            top.connect_to_top_left(top_prev.top_left)
            top.connect_to_bottom_left(top_prev.bottom_left)
        else:
            top.connect_to_top_left(top_left)
            top.connect_to_top_right(top_right)
            if s.position(left_point) == Position.ABOVE:
                top.connect_to_bottom_left(top_prev)

        if bottom_prev.up is bottom.up and bottom_prev.down is bottom.down:
            bottom = Trapezoid(bottom_prev.left, bottom.right, bottom.up, bottom.down)
            bottom.connect_to_top_left(bottom_prev.top_left)
            top.connect_to_bottom_left(bottom_prev.bottom_left)
        else:
            bottom.connect_to_bottom_left(bottom_left)
            bottom.connect_to_bottom_right(bottom_right)
            if s.position(left_point) == Position.BELOW:
                bottom.connect_to_top_left(bottom_prev)

    @staticmethod
    def divide_middle_trapezoid(trapezoid: Trapezoid, s: Segment, top_prev: Trapezoid, bottom_prev: Trapezoid):
        upper_segment = trapezoid.up
        lower_segment = trapezoid.down
        right_point = trapezoid.right
        left_point = trapezoid.left

        top = Trapezoid(left_point, right_point, upper_segment, s)
        bottom = Trapezoid(left_point, right_point, s, lower_segment)

        TrapezoidalMap.connect_or_merge_to_previous_trapezoids(trapezoid, top, bottom, top_prev, bottom_prev, s)

        return top, bottom

    @staticmethod
    def divide_rightmost_trapezoid(trapezoid: Trapezoid, s: Segment, top_prev: Trapezoid, bottom_prev: Trapezoid):
        _, q = s.get_points()
        top_right = trapezoid.top_right
        bottom_right = trapezoid.bottom_right
        upper_segment = trapezoid.up
        lower_segment = trapezoid.down
        right_point = trapezoid.right

        top = Trapezoid(q, right_point, upper_segment, s)
        bottom = Trapezoid(q, right_point, s, lower_segment)

        top.top_right = top_right
        bottom.bottom_right = bottom_right

        right = TrapezoidalMap.get_right_trapezoid(trapezoid, top, bottom, s)

        TrapezoidalMap.connect_or_merge_to_previous_trapezoids(trapezoid, top, bottom, top_prev, bottom_prev, s)

        return top, bottom, right

    def update_map(self, trapezoids: list[Trapezoid], s: Segment):
        if len(trapezoids) == 1:
            top, bottom, left, right = TrapezoidalMap.divide_single_trapezoid(trapezoids[0], s)
            trapezoids[0].leaf = Leaf(trapezoids[0])
            self.tree.update_single(trapezoids[0], s, top, bottom, left, right)
        else:
            splitted_trapezoids = []

            top_prev, bottom_prev, left_prev = TrapezoidalMap.divide_leftmost_trapezoid(trapezoids[0], s)
            self.tree.update_single(trapezoids[0], s, top_prev, bottom_prev, left_prev, None)

            for i in range(1, len(trapezoids) - 1):
                top_prev, bottom_prev = TrapezoidalMap.divide_middle_trapezoid(trapezoids[i], s, top_prev, bottom_prev)
                splitted_trapezoids.append((top_prev, bottom_prev))

            self.tree.update_multiple(trapezoids[1:-2:], s, splitted_trapezoids)

            top_prev, bottom_prev, right_prev = TrapezoidalMap.divide_rightmost_trapezoid(trapezoids[-1], s, top_prev, bottom_prev)
            self.tree.update_single(trapezoids[-1], s, top_prev, bottom_prev, None, right_prev)

    @staticmethod
    def __create_segments(permuted_s) -> list[Segment]:
        result = []
        for line in permuted_s:
            start = Point(line[0][0], line[0][1])
            end = Point(line[1][0], line[1][1])
            result.append(Segment(start, end))

        return result

    def __create_rect_bound(self) -> Trapezoid:
        # assuming that segments is list of Segments objects
        min_x = min(self.segments, key=lambda x: x.left.x).left.x
        max_x = max(self.segments, key=lambda x: x.right.x).right.x

        min_y_start = min(self.segments, key=lambda y: y.left.y).left.y
        min_y_end = min(self.segments, key=lambda y: y.right.y).right.y
        max_y_start = max(self.segments, key=lambda y: y.left.y).left.y
        max_y_end = max(self.segments, key=lambda y: y.right.y).right.y

        min_y = min(min_y_start, min_y_end)
        max_y = max(max_y_start, max_y_end)

        topSegment = Segment(Point(min_x, max_y), Point(max_x, max_y))
        bottomSegment = Segment(Point(min_x, min_y), Point(max_x, min_y))

        return Trapezoid(Point(min_x, min_y), Point(max_x, max_y), topSegment, bottomSegment)

    def get_visualizer(self) -> Visualizer:
        visited = set()
        queue = [self.tree.root.trapezoid]
        vis = Visualizer()

        while queue:
            trapezoid = queue.pop(0)

            if trapezoid in visited:
                continue

            visited.add(trapezoid)

            line_segments = trapezoid.get_segments(as_tuples=True)
            vis.add_line_segment(line_segments)

            for neighbor in [trapezoid.top_left, trapezoid.bottom_left, trapezoid.bottom_right,
                             trapezoid.top_right]:
                if neighbor and neighbor not in visited:
                    queue.append(neighbor)

        return vis





