"""Utilities for testing with shapely geometries."""

from ._typing import ArrayLike, OptGeoArrayLike

__all__ = ["assert_geometries_equal"]

def assert_geometries_equal(
    x: OptGeoArrayLike,
    y: OptGeoArrayLike,
    tolerance: ArrayLike[float] = 1e-7,
    equal_none: bool = True,
    equal_nan: bool = True,
    normalize: bool = False,
    err_msg: str = "",
    verbose: bool = True,
) -> None:
    """Raise an AssertionError if two geometry array_like objects are not equal.

    Given two array_like objects, check that the shape is equal and all elements
    of these objects are equal. An exception is raised at shape mismatch or
    conflicting values. In contrast to the standard usage in shapely, no
    assertion is raised if both objects have NaNs/Nones in the same positions.

    Parameters
    ----------
    x, y : Geometry or array_like
        Geometry or geometries to compare.
    tolerance: float, default 1e-7
        The tolerance to use when comparing geometries.
    equal_none : bool, default True
        Whether to consider None elements equal to other None elements.
    equal_nan : bool, default True
        Whether to consider nan coordinates as equal to other nan coordinates.
    normalize : bool, default False
        Whether to normalize geometries prior to comparison.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.

    """
