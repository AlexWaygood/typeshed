from _typeshed import SupportsItems
from collections.abc import Iterable, Iterator
from typing import Any, Protocol, TypeVar

_KT_co = TypeVar("_KT_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)
_T = TypeVar("_T")

class _SupportsItemsAndLen(SupportsItems[_KT_co, _VT_co], Protocol[_KT_co, _VT_co]):
    def __len__(self) -> int: ...

class CircularDependencyError(ValueError):
    data: dict[Any, set[Any]]
    def __init__(self, data: dict[Any, set[Any]]) -> None: ...

def toposort(data: _SupportsItemsAndLen[_T, Iterable[_T]]) -> Iterator[set[_T]]:
    """Dependencies are expressed as a dictionary whose keys are items
    and whose values are a set of dependent items. Output is a list of
    sets in topological order. The first set consists of items with no
    dependences, each subsequent set consists of items that depend upon
    items in the preceeding sets.
    """

def toposort_flatten(data: _SupportsItemsAndLen[_T, Iterable[_T]], sort: bool = ...) -> list[_T]:
    """Returns a single list of dependencies. For any set returned by
    toposort(), those items are sorted and appended to the result (just to
    make the results deterministic).
    """

__all__ = ["toposort", "toposort_flatten", "CircularDependencyError"]
