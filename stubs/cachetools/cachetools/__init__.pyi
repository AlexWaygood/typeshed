"""Extensible memoizing collections and decorators."""

from _typeshed import IdentityFunction, Unused
from collections.abc import Callable, Iterator, MutableMapping, Sequence
from contextlib import AbstractContextManager
from threading import Condition
from typing import Any, TypeVar, overload
from typing_extensions import deprecated

__all__ = ("Cache", "FIFOCache", "LFUCache", "LRUCache", "RRCache", "TLRUCache", "TTLCache", "cached", "cachedmethod")
__version__: str

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_T = TypeVar("_T")

class Cache(MutableMapping[_KT, _VT]):
    """Mutable mapping to serve as a simple cache or cache base class."""

    @overload
    def __init__(self, maxsize: float, getsizeof: Callable[[_VT], float]) -> None: ...
    @overload
    def __init__(self, maxsize: float, getsizeof: None = None) -> None: ...
    def __getitem__(self, key: _KT) -> _VT: ...
    def __setitem__(self, key: _KT, value: _VT) -> None: ...
    def __delitem__(self, key: _KT) -> None: ...
    def __missing__(self, key: _KT) -> _VT: ...
    def __iter__(self) -> Iterator[_KT]: ...
    def __len__(self) -> int: ...
    @overload
    def pop(self, key: _KT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _VT | _T) -> _VT | _T: ...
    def setdefault(self, key: _KT, default: _VT | None = None) -> _VT: ...
    @property
    def maxsize(self) -> float:
        """The maximum size of the cache."""

    @property
    def currsize(self) -> float:
        """The current size of the cache."""

    @staticmethod
    def getsizeof(value: _VT) -> float:
        """Return the size of a cache element's value."""

class FIFOCache(Cache[_KT, _VT]):
    """First In First Out (FIFO) cache implementation."""

class LFUCache(Cache[_KT, _VT]):
    """Least Frequently Used (LFU) cache implementation."""

class LRUCache(Cache[_KT, _VT]):
    """Least Recently Used (LRU) cache implementation."""

class RRCache(Cache[_KT, _VT]):
    """Random Replacement (RR) cache implementation."""

    @overload
    def __init__(self, maxsize: float, choice: None = None, getsizeof: None = None) -> None: ...
    @overload
    def __init__(self, maxsize: float, *, getsizeof: Callable[[_VT], float]) -> None: ...
    @overload
    def __init__(self, maxsize: float, choice: None, getsizeof: Callable[[_VT], float]) -> None: ...
    @overload
    def __init__(self, maxsize: float, choice: Callable[[Sequence[_KT]], _KT], getsizeof: None = None) -> None: ...
    @overload
    def __init__(self, maxsize: float, choice: Callable[[Sequence[_KT]], _KT], getsizeof: Callable[[_VT], float]) -> None: ...
    @property
    def choice(self) -> Callable[[Sequence[_KT]], _KT]:
        """The `choice` function used by the cache."""

class _TimedCache(Cache[_KT, _VT]):
    """Base class for time aware cache implementations."""

    @overload
    def __init__(self, maxsize: float, timer: Callable[[], float] = ..., getsizeof: None = None) -> None: ...
    @overload
    def __init__(self, maxsize: float, timer: Callable[[], float], getsizeof: Callable[[_VT], float]) -> None: ...
    @overload
    def __init__(self, maxsize: float, timer: Callable[[], float] = ..., *, getsizeof: Callable[[_VT], float]) -> None: ...
    @property
    def currsize(self) -> float: ...

    class _Timer:
        def __init__(self, timer: Callable[[], float]) -> None: ...
        def __call__(self) -> float: ...
        def __enter__(self) -> float: ...
        def __exit__(self, *exc: Unused) -> None: ...

    @property
    def timer(self) -> _Timer:
        """The timer function used by the cache."""

class TTLCache(_TimedCache[_KT, _VT]):
    """LRU Cache implementation with per-item time-to-live (TTL) value."""

    @overload
    def __init__(self, maxsize: float, ttl: float, timer: Callable[[], float] = ..., getsizeof: None = None) -> None: ...
    @overload
    def __init__(self, maxsize: float, ttl: float, timer: Callable[[], float], getsizeof: Callable[[_VT], float]) -> None: ...
    @overload
    def __init__(
        self, maxsize: float, ttl: float, timer: Callable[[], float] = ..., *, getsizeof: Callable[[_VT], float]
    ) -> None: ...
    @property
    def ttl(self) -> float:
        """The time-to-live value of the cache's items."""

    def expire(self, time: float | None = None) -> list[tuple[_KT, _VT]]:
        """Remove expired items from the cache and return an iterable of the
        expired `(key, value)` pairs.

        """

class TLRUCache(_TimedCache[_KT, _VT]):
    """Time aware Least Recently Used (TLRU) cache implementation."""

    def __init__(
        self,
        maxsize: float,
        ttu: Callable[[_KT, _VT, float], float],
        timer: Callable[[], float] = ...,
        getsizeof: Callable[[_VT], float] | None = None,
    ) -> None: ...
    @property
    def ttu(self) -> Callable[[_KT, _VT, float], float]:
        """The local time-to-use function used by the cache."""

    def expire(self, time: float | None = None) -> list[tuple[_KT, _VT]]:
        """Remove expired items from the cache and return an iterable of the
        expired `(key, value)` pairs.

        """

@overload
def cached(
    cache: MutableMapping[_KT, Any] | None,
    key: Callable[..., _KT] = ...,
    lock: AbstractContextManager[Any] | None = None,
    condition: Condition | None = None,
    info: bool = False,
) -> IdentityFunction:
    """Decorator to wrap a function with a memoizing callable that saves
    results in a cache.

    """

@overload
@deprecated("Passing `info` as positional parameter is deprecated.")
def cached(
    cache: MutableMapping[_KT, Any] | None,
    key: Callable[..., _KT] = ...,
    lock: AbstractContextManager[Any] | None = None,
    condition: bool | None = None,
) -> IdentityFunction: ...
def cachedmethod(
    cache: Callable[[Any], MutableMapping[_KT, Any] | None],
    key: Callable[..., _KT] = ...,
    lock: Callable[[Any], AbstractContextManager[Any]] | None = None,
    condition: Condition | None = None,
) -> IdentityFunction:
    """Decorator to wrap a class or instance method with a memoizing
    callable that saves results in a cache.

    """
