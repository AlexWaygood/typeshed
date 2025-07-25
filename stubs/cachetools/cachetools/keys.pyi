"""Key functions for memoizing decorators."""

from _typeshed import Unused
from collections.abc import Hashable

__all__ = ("hashkey", "methodkey", "typedkey", "typedmethodkey")

def hashkey(*args: Hashable, **kwargs: Hashable) -> tuple[Hashable, ...]:
    """Return a cache key for the specified hashable arguments."""

def methodkey(self: Unused, *args: Hashable, **kwargs: Hashable) -> tuple[Hashable, ...]:
    """Return a cache key for use with cached methods."""

def typedkey(*args: Hashable, **kwargs: Hashable) -> tuple[Hashable, ...]:
    """Return a typed cache key for the specified hashable arguments."""

def typedmethodkey(self: Unused, *args: Hashable, **kwargs: Hashable) -> tuple[Hashable, ...]:
    """Return a typed cache key for use with cached methods."""
