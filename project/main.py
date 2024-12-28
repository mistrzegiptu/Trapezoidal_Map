from visualizer.main import Visualizer
from src.data_structures import *

if __name__ == "__main__":
    t = Trapezoid(Point(1, 1), Point(2, 1), Segment(Point(1, 1), Point(2, 1)), Segment(Point(1, 2), Point(2, 2)))
    vis = Visualizer()
    vis.add_line_segment(t.get_segments(as_tuples=True))
    vis.show()