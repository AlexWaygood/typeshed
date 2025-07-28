"""
PDFPathObject is an efficient way to draw paths on a Canvas. Do not
instantiate directly, obtain one from the Canvas instead.

Progress Reports:
8.83, 2000-01-13, gmcm: created from pdfgen.py

"""

from typing import Final

__version__: Final[str]

class PDFPathObject:
    """Represents a graphic path.  There are certain 'modes' to PDF
    drawing, and making a separate object to expose Path operations
    ensures they are completed with no run-time overhead.  Ask
    the Canvas for a PDFPath with getNewPathObject(); moveto/lineto/
    curveto wherever you want; add whole shapes; and then add it back
    into the canvas with one of the relevant operators.

    Path objects are probably not long, so we pack onto one line

    the code argument allows a canvas to get the operations appended directly so
    avoiding the final getCode
    """

    def __init__(self, code=None) -> None: ...
    def getCode(self):
        """pack onto one line; used internally"""

    def moveTo(self, x, y) -> None: ...
    def lineTo(self, x, y) -> None: ...
    def curveTo(self, x1, y1, x2, y2, x3, y3) -> None: ...
    def arc(self, x1, y1, x2, y2, startAng: int = 0, extent: int = 90) -> None:
        """Contributed to piddlePDF by Robert Kern, 28/7/99.
        Draw a partial ellipse inscribed within the rectangle x1,y1,x2,y2,
        starting at startAng degrees and covering extent degrees.   Angles
        start with 0 to the right (+x) and increase counter-clockwise.
        These should have x1<x2 and y1<y2.

        The algorithm is an elliptical generalization of the formulae in
        Jim Fitzsimmon's TeX tutorial <URL: http://www.tinaja.com/bezarc1.pdf>.
        """

    def arcTo(self, x1, y1, x2, y2, startAng: int = 0, extent: int = 90) -> None:
        """Like arc, but draws a line from the current point to
        the start if the start is not the current point.
        """

    def rect(self, x, y, width, height) -> None:
        """Adds a rectangle to the path"""

    def ellipse(self, x, y, width, height) -> None:
        """adds an ellipse to the path"""

    def circle(self, x_cen, y_cen, r) -> None:
        """adds a circle to the path"""

    def roundRect(self, x, y, width, height, radius) -> None:
        """Draws a rectangle with rounded corners. The corners are
        approximately quadrants of a circle, with the given radius.
        """

    def close(self) -> None:
        """draws a line back to where it started"""
