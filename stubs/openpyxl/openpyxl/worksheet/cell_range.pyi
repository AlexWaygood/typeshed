from _typeshed import ConvertibleToInt, Incomplete
from collections.abc import Generator, Iterator
from itertools import product
from typing import Any, Literal, overload

from openpyxl.descriptors import Strict
from openpyxl.descriptors.base import MinMax
from openpyxl.descriptors.serialisable import Serialisable

class CellRange(Serialisable):
    """
    Represents a range in a sheet: title and coordinates.

    This object is used to perform operations on ranges, like:

    - shift, expand or shrink
    - union/intersection with another sheet range,

    We can check whether a range is:

    - equal or not equal to another,
    - disjoint of another,
    - contained in another.

    We can get:

    - the size of a range.
    - the range bounds (vertices)
    - the coordinates,
    - the string representation,

    """

    min_col: MinMax[int, Literal[False]]
    min_row: MinMax[int, Literal[False]]
    max_col: MinMax[int, Literal[False]]
    max_row: MinMax[int, Literal[False]]
    title: str | None

    # With `range_string`, min/max parameters go unused.
    # Enforcing `None` to avoid confusion upon which params get used
    # if the user still tries to pass a `ConvertibleToInt`.
    @overload
    def __init__(
        self,
        range_string: str,
        min_col: None = None,
        min_row: None = None,
        max_col: None = None,
        max_row: None = None,
        title: str | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        range_string: None = None,
        *,
        min_col: ConvertibleToInt,
        min_row: ConvertibleToInt,
        max_col: ConvertibleToInt,
        max_row: ConvertibleToInt,
        title: str | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        range_string: None,
        min_col: ConvertibleToInt,
        min_row: ConvertibleToInt,
        max_col: ConvertibleToInt,
        max_row: ConvertibleToInt,
        title: str | None = None,
    ) -> None: ...
    @property
    def bounds(self) -> tuple[int, int, int, int]:
        """
        Vertices of the range as a tuple
        """

    @property
    def coord(self) -> str:
        """
        Excel-style representation of the range
        """

    @property
    def rows(self) -> Generator[list[tuple[int, int]], None, None]:
        """
        Return cell coordinates as rows
        """

    @property
    def cols(self) -> Generator[list[tuple[int, int]], None, None]:
        """
        Return cell coordinates as columns
        """

    @property
    def cells(self) -> product[tuple[int, int]]: ...
    def __copy__(self): ...
    def shift(self, col_shift: int = 0, row_shift: int = 0) -> None:
        """
        Shift the focus of the range according to the shift values (*col_shift*, *row_shift*).

        :type col_shift: int
        :param col_shift: number of columns to be moved by, can be negative
        :type row_shift: int
        :param row_shift: number of rows to be moved by, can be negative
        :raise: :class:`ValueError` if any row or column index < 1
        """

    def __ne__(self, other: object) -> bool:
        """
        Test whether the ranges are not equal.

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range
        :return: ``True`` if *range* != *other*.
        """

    def __eq__(self, other: object) -> bool:
        """
        Test whether the ranges are equal.

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range
        :return: ``True`` if *range* == *other*.
        """

    def issubset(self, other: CellRange) -> bool:
        """
        Test whether every cell in this range is also in *other*.

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range
        :return: ``True`` if *range* <= *other*.
        """
    __le__ = issubset
    def __lt__(self, other: CellRange) -> bool:
        """
        Test whether *other* contains every cell of this range, and more.

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range
        :return: ``True`` if *range* < *other*.
        """

    def issuperset(self, other: CellRange) -> bool:
        """
        Test whether every cell in *other* is in this range.

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range
        :return: ``True`` if *range* >= *other* (or *other* in *range*).
        """
    __ge__ = issuperset
    def __contains__(self, coord: str) -> bool:
        """
        Check whether the range contains a particular cell coordinate
        """

    def __gt__(self, other: CellRange) -> bool:
        """
        Test whether this range contains every cell in *other*, and more.

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range
        :return: ``True`` if *range* > *other*.
        """

    def isdisjoint(self, other: CellRange) -> bool:
        """
        Return ``True`` if this range has no cell in common with *other*.
        Ranges are disjoint if and only if their intersection is the empty range.

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range.
        :return: ``True`` if the range has no cells in common with other.
        """

    def intersection(self, other):
        """
        Return a new range with cells common to this range and *other*

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range.
        :return: the intersecting sheet range.
        :raise: :class:`ValueError` if the *other* range doesn't intersect
            with this range.
        """
    __and__ = intersection
    def union(self, other):
        """
        Return the minimal superset of this range and *other*. This new range
        will contain all cells from this range, *other*, and any additional
        cells required to form a rectangular ``CellRange``.

        :type other: openpyxl.worksheet.cell_range.CellRange
        :param other: Other sheet range.
        :return: a ``CellRange`` that is a superset of this and *other*.
        """
    __or__ = union
    # Iterates over class attributes. Value could be anything.
    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """
        For use as a dictionary elsewhere in the library.
        """

    def expand(self, right: int = 0, down: int = 0, left: int = 0, up: int = 0) -> None:
        """
        Expand the range by the dimensions provided.

        :type right: int
        :param right: expand range to the right by this number of cells
        :type down: int
        :param down: expand range down by this number of cells
        :type left: int
        :param left: expand range to the left by this number of cells
        :type up: int
        :param up: expand range up by this number of cells
        """

    def shrink(self, right: int = 0, bottom: int = 0, left: int = 0, top: int = 0) -> None:
        """
        Shrink the range by the dimensions provided.

        :type right: int
        :param right: shrink range from the right by this number of cells
        :type down: int
        :param down: shrink range from the top by this number of cells
        :type left: int
        :param left: shrink range from the left by this number of cells
        :type up: int
        :param up: shrink range from the bottom by this number of cells
        """

    @property
    def size(self) -> dict[str, int]:
        """Return the size of the range as a dictionary of rows and columns."""

    @property
    def top(self) -> list[tuple[int, int]]:
        """A list of cell coordinates that comprise the top of the range"""

    @property
    def bottom(self) -> list[tuple[int, int]]:
        """A list of cell coordinates that comprise the bottom of the range"""

    @property
    def left(self) -> list[tuple[int, int]]:
        """A list of cell coordinates that comprise the left-side of the range"""

    @property
    def right(self) -> list[tuple[int, int]]:
        """A list of cell coordinates that comprise the right-side of the range"""

class MultiCellRange(Strict):
    ranges: Incomplete
    def __init__(self, ranges=...) -> None: ...
    def __contains__(self, coord: str | CellRange) -> bool: ...
    def sorted(self) -> list[CellRange]:
        """
        Return a sorted list of items
        """

    def add(self, coord) -> None:
        """
        Add a cell coordinate or CellRange
        """

    def __iadd__(self, coord): ...
    def __eq__(self, other: str | MultiCellRange) -> bool: ...  # type: ignore[override]
    def __ne__(self, other: str | MultiCellRange) -> bool: ...  # type: ignore[override]
    def __bool__(self) -> bool: ...
    def remove(self, coord) -> None: ...
    def __iter__(self) -> Iterator[CellRange]: ...
    def __copy__(self): ...
