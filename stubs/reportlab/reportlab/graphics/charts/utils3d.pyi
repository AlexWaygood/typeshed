from _typeshed import Incomplete

class _YStrip:
    y0: Incomplete
    y1: Incomplete
    slope: Incomplete
    fillColor: Incomplete
    fillColorShaded: Incomplete
    def __init__(self, y0, y1, slope, fillColor, fillColorShaded, shading: float = 0.1) -> None: ...

def mod_2pi(radians): ...

class _Segment:
    a: Incomplete
    b: Incomplete
    x0: Incomplete
    x1: Incomplete
    y0: Incomplete
    y1: Incomplete
    series: Incomplete
    i: Incomplete
    s: Incomplete
    def __init__(self, s, i, data) -> None: ...
    def intersect(self, o, I):
        """try to find an intersection with _Segment o"""

def find_intersections(data, small: int = 0):
    """
    data is a sequence of series
    each series is a list of (x,y) coordinates
    where x & y are ints or floats

    find_intersections returns a sequence of 4-tuples
        i, j, x, y

    where i is a data index j is an insertion position for data[i]
    and x, y are coordinates of an intersection of series data[i]
    with some other series. If correctly implemented we get all such
    intersections. We don't count endpoint intersections and consider
    parallel lines as non intersecting (even when coincident).
    We ignore segments that have an estimated size less than small.
    """
