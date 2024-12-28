from data_structures import *
import random

class TrapezoidalMap:

    def __init__(self, S: list[tuple[tuple[float, float], tuple[float, float]]]):
        permuted_s = random.sample(S, len(S))
        self.segments = self.__create_segments(permuted_s)
        self.rect_bound = self.__create_rect_bound()
        self.tree = DTree()
        self.tree.root = self.rect_bound

#   TODO: Dlaczego nic nie zwraca?
    def build_trapezoidal_map(self):
        for i in range(len(self.segments)):
            intersected_trapezoids = self.follow_segment(self.segments[i])

        return 0

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
