from collections.abc import Iterable
from typing import TypeVar

_T = TypeVar("_T")

class IndexedList(list[_T]):
    """
    List with optimised access by value
    Based on Alex Martelli's recipe

    http://code.activestate.com/recipes/52303-the-auxiliary-dictionary-idiom-for-sequences-with-/
    """

    clean: bool
    def __init__(self, iterable: Iterable[_T] | None = None) -> None: ...
    def __contains__(self, value: object) -> bool: ...
    def index(self, value: _T) -> int: ...  # type: ignore[override]
    def append(self, value: _T) -> None: ...
    def add(self, value: _T) -> int: ...
