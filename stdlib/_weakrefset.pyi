import sys
from collections.abc import Iterable, Iterator, MutableSet, Set as AbstractSet
from typing import Any, TypeVar, overload
from typing_extensions import Self

if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = ["WeakSet"]

_S = TypeVar("_S")
_T = TypeVar("_T")

class WeakSet(MutableSet[_T]):
    @overload
    def __init__(self, data: None = None) -> None: ...
    @overload
    def __init__(self, data: Iterable[_T]) -> None: ...
    def add(self, item: _T) -> None: ...
    def discard(self, item: _T | None) -> None: ...
    def copy(self) -> Self: ...
    def remove(self, item: _T) -> None: ...
    def update(self, other: Iterable[_T]) -> None: ...
    def __contains__(self, item: object) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __ior__(self, other: Iterable[_T]) -> Self: ...  # type: ignore[override,misc]
    def difference(self, other: Iterable[_T]) -> Self: ...
    @overload  # type: ignore[override]
    def __sub__(self: AbstractSet[_S | None], other: Iterable[None]) -> WeakSet[_S]: ...  # type: ignore[overload-overlap]
    @overload
    def __sub__(self, other: Iterable[_T | None]) -> Self: ...
    def difference_update(self, other: Iterable[_T | None]) -> None: ...
    def __isub__(self, other: Iterable[_T | None]) -> Self: ...  # type: ignore[misc]
    def intersection(self, other: Iterable[_T]) -> Self: ...
    def __and__(self, other: Iterable[Any]) -> Self: ...
    def intersection_update(self, other: Iterable[Any]) -> None: ...
    def __iand__(self, other: Iterable[Any]) -> Self: ...
    def issubset(self, other: Iterable[_T]) -> bool: ...
    def __le__(self, other: Iterable[_T]) -> bool: ...
    def __lt__(self, other: Iterable[_T]) -> bool: ...
    def issuperset(self, other: Iterable[_T]) -> bool: ...
    def __ge__(self, other: Iterable[_T]) -> bool: ...
    def __gt__(self, other: Iterable[_T]) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def symmetric_difference(self, other: Iterable[_S]) -> WeakSet[_S | _T]: ...
    def __xor__(self, other: Iterable[_S]) -> WeakSet[_S | _T]: ...
    def symmetric_difference_update(self, other: Iterable[_T]) -> None: ...
    def __ixor__(self, other: Iterable[_T]) -> Self: ...  # type: ignore[override,misc]
    def union(self, other: Iterable[_S]) -> WeakSet[_S | _T]: ...
    def __or__(self, other: Iterable[_S]) -> WeakSet[_S | _T]: ...
    def isdisjoint(self, other: Iterable[_T]) -> bool: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...
