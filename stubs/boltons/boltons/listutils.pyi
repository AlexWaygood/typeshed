"""Python's builtin :class:`list` is a very fast and efficient
sequence type, but it could be better for certain access patterns,
such as non-sequential insertion into a large lists. ``listutils``
provides a pure-Python solution to this problem.

For utilities for working with iterables and lists, check out
:mod:`iterutils`. For the a :class:`list`-based version of
:class:`collections.namedtuple`, check out :mod:`namedutils`.
"""

from collections.abc import Iterable
from typing import SupportsIndex, TypeVar
from typing_extensions import Self, TypeAlias

_T = TypeVar("_T")

class BarrelList(list[_T]):
    """The ``BarrelList`` is a :class:`list` subtype backed by many
    dynamically-scaled sublists, to provide better scaling and random
    insertion/deletion characteristics. It is a subtype of the builtin
    :class:`list` and has an identical API, supporting indexing,
    slicing, sorting, etc. If application requirements call for
    something more performant, consider the `blist module available on
    PyPI`_.

    The name comes by way of Kurt Rose, who said it reminded him of
    barrel shifters. Not sure how, but it's BList-like, so the name
    stuck. BList is of course a reference to `B-trees`_.

    Args:
        iterable: An optional iterable of initial values for the list.

    >>> blist = BList(range(100000))
    >>> blist.pop(50000)
    50000
    >>> len(blist)
    99999
    >>> len(blist.lists)  # how many underlying lists
    8
    >>> slice_idx = blist.lists[0][-1]
    >>> blist[slice_idx:slice_idx + 2]
    BarrelList([11637, 11638])

    Slicing is supported and works just fine across list borders,
    returning another instance of the BarrelList.

    .. _blist module available on PyPI: https://pypi.python.org/pypi/blist
    .. _B-trees: https://en.wikipedia.org/wiki/B-tree

    """

    lists: list[list[_T]]
    def __init__(self, iterable: Iterable[_T] | None = None) -> None: ...
    def insert(self, index: SupportsIndex, item: _T) -> None: ...
    def append(self, item: _T) -> None: ...
    def extend(self, iterable: Iterable[_T]) -> None: ...
    def pop(self, *a) -> _T: ...
    def iter_slice(self, start: int | None, stop: int | None, step: int | None = None) -> Iterable[_T]: ...
    def del_slice(self, start: int, stop: int, step: int | None = None) -> None: ...
    __delslice__ = del_slice
    @classmethod
    def from_iterable(cls, it: Iterable[_T]) -> Self: ...
    def __getslice__(self, start: int, stop: int): ...
    def __setslice__(self, start: SupportsIndex, stop: SupportsIndex, sequence: Iterable[_T]) -> None: ...
    def sort(self) -> None: ...  # type: ignore[override]
    def reverse(self) -> None: ...
    def count(self, item: _T) -> int: ...
    def index(self, item: _T) -> int: ...  # type: ignore[override]

BList: TypeAlias = BarrelList[_T]

class SplayList(list[_T]):
    """Like a `splay tree`_, the SplayList facilitates moving higher
    utility items closer to the front of the list for faster access.

    .. _splay tree: https://en.wikipedia.org/wiki/Splay_tree
    """

    def shift(self, item_index: int, dest_index: int = 0) -> None: ...
    def swap(self, item_index: SupportsIndex, dest_index: SupportsIndex) -> None: ...

__all__ = ["BList", "BarrelList"]
