from data_structures import *
import random

class TrapezoidalMap:

    def __init__(self, S: list[tuple[tuple[float, float], tuple[float, float]]]):
        permuted_s = random.sample(S, len(S))
        self.segments = self._create_segments(permuted_s)
        self.rect_bound = self._create_rect_bound()
        self.tree = DTree()


    def build_trapezoidal_map(self):
        # TODO tomorrow
        return 0

    def _create_segments(self, permuted_s) -> list[Segment]:
        result = []
        for line in permuted_s:
            start = Point(line[0][0], line[0][1])
            end = Point(line[1][0], line[1][1])
            result.append(Segment(start, end))

        return result

    def _create_rect_bound(self) -> Trapezoid:
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
