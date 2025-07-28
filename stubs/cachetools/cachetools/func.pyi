"""`functools.lru_cache` compatible memoizing function decorators."""

from _typeshed import IdentityFunction
from collections.abc import Callable, Sequence
from typing import TypeVar

__all__ = ("fifo_cache", "lfu_cache", "lru_cache", "rr_cache", "ttl_cache")
_T = TypeVar("_T")

def fifo_cache(maxsize: float | None = 128, typed: bool = False) -> IdentityFunction:
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a First In First Out (FIFO)
    algorithm.

    """

def lfu_cache(maxsize: float | None = 128, typed: bool = False) -> IdentityFunction:
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Frequently Used (LFU)
    algorithm.

    """

def lru_cache(maxsize: float | None = 128, typed: bool = False) -> IdentityFunction:
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Recently Used (LRU)
    algorithm.

    """

def rr_cache(
    maxsize: float | None = 128, choice: Callable[[Sequence[_T]], _T] | None = ..., typed: bool = False
) -> IdentityFunction:
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Random Replacement (RR)
    algorithm.

    """

def ttl_cache(
    maxsize: float | None = 128, ttl: float = 600, timer: Callable[[], float] = ..., typed: bool = False
) -> IdentityFunction:
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Recently Used (LRU)
    algorithm with a per-item time-to-live (TTL) value.
    """
