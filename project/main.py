from src.trapezoidal_map import TrapezoidalMap
from src.data_structures import Segment, Point, Trapezoid, Leaf

t = TrapezoidalMap([((33333.333333333336, 0.0), (77777.77777777778, 0.0)), ((11111.111111111111, 20000.0), (100000.0, 20000.0)), ((0.0, 60000.0), (55555.555555555555, 60000.0)), ((44444.444444444445, 80000.0), (66666.66666666667, 80000.0)), ((22222.222222222223, 40000.0), (88888.88888888889, 40000.0))])
t.build_trapezoidal_map()
vis = t.vis
vis.save_gif()
