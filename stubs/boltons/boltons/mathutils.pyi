"""This module provides useful math functions on top of Python's
built-in :mod:`math` module.
"""

from collections.abc import Iterable
from typing import overload

def clamp(x: float, lower: float = ..., upper: float = ...) -> float:
    """Limit a value to a given range.

    Args:
        x (int or float): Number to be clamped.
        lower (int or float): Minimum value for x.
        upper (int or float): Maximum value for x.

    The returned value is guaranteed to be between *lower* and
    *upper*. Integers, floats, and other comparable types can be
    mixed.

    >>> clamp(1.0, 0, 5)
    1.0
    >>> clamp(-1.0, 0, 5)
    0
    >>> clamp(101.0, 0, 5)
    5
    >>> clamp(123, upper=5)
    5

    Similar to `numpy's clip`_ function.

    .. _numpy's clip: http://docs.scipy.org/doc/numpy/reference/generated/numpy.clip.html

    """

@overload
def ceil(x: float, options: None = None) -> int:
    """Return the ceiling of *x*. If *options* is set, return the smallest
    integer or float from *options* that is greater than or equal to
    *x*.

    Args:
        x (int or float): Number to be tested.
        options (iterable): Optional iterable of arbitrary numbers
          (ints or floats).

    >>> VALID_CABLE_CSA = [1.5, 2.5, 4, 6, 10, 25, 35, 50]
    >>> ceil(3.5, options=VALID_CABLE_CSA)
    4
    >>> ceil(4, options=VALID_CABLE_CSA)
    4
    """

@overload
def ceil(x: float, options: Iterable[float]) -> float: ...
@overload
def floor(x: float, options: None = None) -> int:
    """Return the floor of *x*. If *options* is set, return the largest
    integer or float from *options* that is less than or equal to
    *x*.

    Args:
        x (int or float): Number to be tested.
        options (iterable): Optional iterable of arbitrary numbers
          (ints or floats).

    >>> VALID_CABLE_CSA = [1.5, 2.5, 4, 6, 10, 25, 35, 50]
    >>> floor(3.5, options=VALID_CABLE_CSA)
    2.5
    >>> floor(2.5, options=VALID_CABLE_CSA)
    2.5

    """

@overload
def floor(x: float, options: Iterable[float]) -> float: ...

class Bits:
    """
    An immutable bit-string or bit-array object.
    Provides list-like access to bits as bools,
    as well as bitwise masking and shifting operators.
    Bits also make it easy to convert between many
    different useful representations:

    * bytes -- good for serializing raw binary data
    * int -- good for incrementing (e.g. to try all possible values)
    * list of bools -- good for iterating over or treating as flags
    * hex/bin string -- good for human readability

    """

    val: int
    len: int
    def __init__(self, val: int | list[bool] | str | bytes = 0, len_: int | None = None) -> None: ...
    def __getitem__(self, k) -> Bits | bool: ...
    def __len__(self) -> int: ...
    def __eq__(self, other) -> bool: ...
    def __or__(self, other: Bits) -> Bits: ...
    def __and__(self, other: Bits) -> Bits: ...
    def __lshift__(self, other: int) -> Bits: ...
    def __rshift__(self, other: int) -> Bits: ...
    def __hash__(self) -> int: ...
    def as_list(self) -> list[bool]: ...
    def as_bin(self) -> str: ...
    def as_hex(self) -> str: ...
    def as_int(self) -> int: ...
    def as_bytes(self) -> bytes: ...
    @classmethod
    def from_list(cls, list_): ...
    @classmethod
    def from_bin(cls, bin): ...
    @classmethod
    def from_hex(cls, hex): ...
    @classmethod
    def from_int(cls, int_, len_: int | None = None): ...
    @classmethod
    def from_bytes(cls, bytes_): ...
