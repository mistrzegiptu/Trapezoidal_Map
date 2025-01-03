from src.trapezoidal_map import TrapezoidalMap
from src.data_structures import Segment, Point, Trapezoid, Leaf

t = TrapezoidalMap([((1, 2), (2, 2.5)), ((1.5, 3), (2.5, 3.5))])
t.build_trapezoidal_map()

vis = t.get_visualizer()
vis.show()
