from collections.abc import Iterator, Mapping as DictMixin
from typing import TypeVar

_T = TypeVar("_T")
_VT = TypeVar("_VT")

class LazyDict(DictMixin[str, _VT]):
    """Dictionary populated on first use."""

    data: dict[str, _VT] | None
    def __getitem__(self, key: str) -> _VT: ...
    def __contains__(self, key: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...

class LazyList(list[_T]):
    """List populated on first use."""

    # does not return `Self` type:
    def __new__(cls, fill_iter=None) -> LazyList[_T]: ...

class LazySet(set[_T]):
    """Set populated on first use."""

    # does not return `Self` type:
    def __new__(cls, fill_iter=None) -> LazySet[_T]: ...
