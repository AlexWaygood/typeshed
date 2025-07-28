"""Collections of polygons and related utilities."""

from collections.abc import Collection
from typing_extensions import Self

from .base import BaseMultipartGeometry
from .multilinestring import MultiLineString
from .polygon import Polygon, _PolygonHolesLike, _PolygonShellLike

__all__ = ["MultiPolygon"]

class MultiPolygon(BaseMultipartGeometry[Polygon]):
    """A collection of one or more Polygons.

    If component polygons overlap the collection is invalid and some
    operations on it may fail.

    Parameters
    ----------
    polygons : sequence
        A sequence of Polygons, or a sequence of (shell, holes) tuples
        where shell is the sequence representation of a linear ring
        (see LinearRing) and holes is a sequence of such linear rings.

    Attributes
    ----------
    geoms : sequence
        A sequence of `Polygon` instances

    Examples
    --------
    Construct a MultiPolygon from a sequence of coordinate tuples

    >>> from shapely import MultiPolygon, Polygon
    >>> ob = MultiPolygon([
    ...     (
    ...     ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)),
    ...     [((0.1,0.1), (0.1,0.2), (0.2,0.2), (0.2,0.1))]
    ...     )
    ... ])
    >>> len(ob.geoms)
    1
    >>> type(ob.geoms[0]) == Polygon
    True

    """

    def __new__(
        self,
        polygons: (
            BaseMultipartGeometry
            | Collection[Polygon | tuple[_PolygonShellLike] | tuple[_PolygonShellLike, _PolygonHolesLike] | None]
            | None
        ) = None,
    ) -> Self:
        """Create a new MultiPolygon geometry."""

    def svg(self, scale_factor: float = 1.0, fill_color: str | None = None, opacity: float | None = None) -> str:  # type: ignore[override]
        """Return group of SVG path elements for the MultiPolygon geometry.

        Parameters
        ----------
        scale_factor : float
            Multiplication factor for the SVG stroke-width.  Default is 1.
        fill_color : str, optional
            Hex string for fill color. Default is to use "#66cc99" if
            geometry is valid, and "#ff3333" if invalid.
        opacity : float
            Float number between 0 and 1 for color opacity. Default value is 0.6

        """
    # more precise base overrides
    @property
    def boundary(self) -> MultiLineString:
        """Return a lower dimension geometry that bounds the object.

        The boundary of a polygon is a line, the boundary of a line is a
        collection of points. The boundary of a point is an empty (null)
        collection.
        """
