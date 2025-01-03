from src.trapezoidal_map import TrapezoidalMap
from src.data_structures import Segment, Point, Trapezoid, Leaf

t = TrapezoidalMap([((0, 0), (1, -1)), ((0, 0),(2, 1)), ((1, -1), (4, 0)), ((3, 3),(4, 0)), ((0, 0), (3.5, 0.1))])
t.build_trapezoidal_map()
