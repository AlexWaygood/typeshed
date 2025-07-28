"""Collections of points and related utilities."""

from collections.abc import Collection
from typing_extensions import Self

from .base import BaseMultipartGeometry
from .collection import GeometryCollection
from .point import Point, _PointLike

__all__ = ["MultiPoint"]

class MultiPoint(BaseMultipartGeometry[Point]):
    """A collection of one or more Points.

    A MultiPoint has zero area and zero length.

    Parameters
    ----------
    points : sequence
        A sequence of Points, or a sequence of (x, y [,z]) numeric coordinate
        pairs or triples, or an array-like of shape (N, 2) or (N, 3).

    Attributes
    ----------
    geoms : sequence
        A sequence of Points

    Examples
    --------
    Construct a MultiPoint containing two Points

    >>> from shapely import MultiPoint, Point
    >>> ob = MultiPoint([[0.0, 0.0], [1.0, 2.0]])
    >>> len(ob.geoms)
    2
    >>> type(ob.geoms[0]) == Point
    True

    """

    # Note on "points" type in `__new__`:
    # * `Collection` here is loose as the expected type should support "__getitem__".
    # * `Sequence` is more correct but it will lead to False positives with common types
    #   like np.ndarray, pd.Index, pd.Series, ...
    # I went with Collection as false negatives seem better to me than false positives in this case
    def __new__(self, points: MultiPoint | Collection[_PointLike] | None = None) -> Self:
        """Create a new MultiPoint geometry."""

    def svg(self, scale_factor: float = 1.0, fill_color: str | None = None, opacity: float | None = None) -> str:  # type: ignore[override]
        """Return a group of SVG circle elements for the MultiPoint geometry.

        Parameters
        ----------
        scale_factor : float
            Multiplication factor for the SVG circle diameters.  Default is 1.
        fill_color : str, optional
            Hex string for fill color. Default is to use "#66cc99" if
            geometry is valid, and "#ff3333" if invalid.
        opacity : float
            Float number between 0 and 1 for color opacity. Default value is 0.6

        """
    # more precise base overrides
    @property
    def boundary(self) -> GeometryCollection:  # empty geometry collection
        """Return a lower dimension geometry that bounds the object.

        The boundary of a polygon is a line, the boundary of a line is a
        collection of points. The boundary of a point is an empty (null)
        collection.
        """
