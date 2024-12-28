from .data_structures import *
from ..visualizer.main import Visualizer
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
        p, q = s.to_tuple()
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

    # TODO: multiple intersected trapezoids, updating Dtree, possibly refactor this method
    def update_map(self, trapezoids: list[Trapezoid], s: Segment):
        p, q = s.to_tuple()

        if len(trapezoids) == 1:
            trapezoid = trapezoids[0]
            top_right = trapezoid.top_right
            top_left = trapezoid.top_left
            bottom_left = trapezoid.bottom_left
            bottom_right = trapezoid.bottom_right
            upper_segment = trapezoid.up
            lower_segment = trapezoid.down

            top = Trapezoid(p, q, upper_segment, s)
            bottom = Trapezoid(p, q, s, lower_segment)
            left = None
            right = None

            if p.x > trapezoid.left.x:
                left = Trapezoid(trapezoid.left, p, upper_segment, lower_segment)
                left.top_left = top_left
                left.bottom_left = bottom_left
                left.top_right = top
                left.bottom_right = bottom

                top.top_left = left
                bottom.bottom_left = left

            if q.x < trapezoid.right.x:
                right = Trapezoid(q, trapezoid.right, upper_segment, lower_segment)
                right.top_right = top_right
                right.bottom_right = bottom_right
                right.top_left = top
                right.bottom_left = bottom

                top.top_right = right
                bottom.bottom_right = right

            if not left:
                left_s = trapezoid.top_left.down
                if not left_s:
                    left_s = trapezoid.bottom_left.up

                if left_s.q.y > p.y:
                    bottom.top_left = top_left
                elif left_s.q.y < p.y:
                    top.bottom_left = bottom_left

            if not right:
                right_s = trapezoid.top_right.down
                if not right_s:
                    right_s = trapezoid.bottom_right.up

                if right_s.p.y > q.y:
                    top.bottom_right = bottom_right
                elif right_s.p.y < q.y:
                    bottom.top_right = top_right


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





