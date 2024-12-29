from .src.trapezoidal_map import TrapezoidalMap
from .src.data_structures import Segment, Point, Trapezoid, Leaf

t = TrapezoidalMap([((1, 2), (2, 2)), ((1, 3), (2, 3))])
vis = t.get_visualizer()
vis.save_gif(filename="f1")
trapezoid = TrapezoidalMap.divide_single_trapezoid(t.tree.root.trapezoid, Segment(Point(1.2, 2.2), Point(1.6, 2.6)), Point(1.2, 2.2), Point(1.6, 2.6))
t.tree.root = Leaf(trapezoid)
vis = t.get_visualizer()
vis.save_gif(filename="f2")
trapezoid = TrapezoidalMap.divide_single_trapezoid(t.tree.root.trapezoid, Segment(Point(1.3, 2.4), Point(1.5, 2.7)), Point(1.3, 2.4), Point(1.5, 2.7))
t.tree.root = Leaf(trapezoid)
vis = t.get_visualizer()
vis.save_gif(filename="f3")
