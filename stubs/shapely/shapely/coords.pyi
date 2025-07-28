"""Coordinate sequence utilities."""

from array import array
from collections.abc import Iterator
from typing import Literal, overload

import numpy as np
from numpy.typing import DTypeLike, NDArray

class CoordinateSequence:
    """Access to coordinate tuples from the parent geometry's coordinate sequence.

    Examples
    --------
    >>> from shapely.wkt import loads
    >>> g = loads('POINT (0.0 0.0)')
    >>> list(g.coords)
    [(0.0, 0.0)]
    >>> g = loads('POINT M (1 2 4)')
    >>> g.coords[:]
    [(1.0, 2.0, 4.0)]

    """

    def __init__(self, coords: NDArray[np.float64]) -> None:
        """Initialize the CoordinateSequence.

        Parameters
        ----------
        coords : array
            The coordinate array.

        """

    def __len__(self) -> int:
        """Return the length of the CoordinateSequence.

        Returns
        -------
        int
            The length of the CoordinateSequence.

        """

    def __iter__(self) -> Iterator[tuple[float, ...]]:
        """Iterate over the CoordinateSequence."""

    @overload
    def __getitem__(self, key: int) -> tuple[float, ...]:
        """Get the item at the specified index or slice.

        Parameters
        ----------
        key : int or slice
            The index or slice.

        Returns
        -------
        tuple or list
            The item at the specified index or slice.

        """

    @overload
    def __getitem__(self, key: slice) -> list[tuple[float, ...]]: ...
    def __array__(self, dtype: DTypeLike | None = None, copy: Literal[True] | None = None) -> NDArray[np.float64]:
        """Return a copy of the coordinate array.

        Parameters
        ----------
        dtype : data-type, optional
            The desired data-type for the array.
        copy : bool, optional
            If None (default) or True, a copy of the array is always returned.
            If False, a ValueError is raised as this is not supported.

        Returns
        -------
        array
            The coordinate array.

        Raises
        ------
        ValueError
            If `copy=False` is specified.

        """

    @property
    def xy(self) -> tuple[array[float], array[float]]:
        """X and Y arrays."""
