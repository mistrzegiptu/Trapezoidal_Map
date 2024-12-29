from .src.trapezoidal_map import TrapezoidalMap
from .src.data_structures import Segment, Point, Trapezoid, Leaf

t = TrapezoidalMap([((1, 2), (2, 2)), ((1, 3), (2, 3))])
vis = t.get_visualizer()

