import sys
from abc import abstractmethod
from typing import (  # noqa: Y022,Y038,Y057
    AbstractSet as Set,
    AsyncGenerator as AsyncGenerator,
    AsyncIterable as AsyncIterable,
    AsyncIterator as AsyncIterator,
    Awaitable as Awaitable,
    ByteString as ByteString,
    Callable as Callable,
    Collection as Collection,
    Container as Container,
    Coroutine as Coroutine,
    Generator as Generator,
    Hashable as Hashable,
    ItemsView as ItemsView,
    Iterable as Iterable,
    Iterator as Iterator,
    KeysView as KeysView,
    Mapping as Mapping,
    MappingView as MappingView,
    MutableMapping as MutableMapping,
    MutableSequence as MutableSequence,
    MutableSet as MutableSet,
    Protocol,
    Reversible as Reversible,
    Sequence as Sequence,
    Sized as Sized,
    ValuesView as ValuesView,
    runtime_checkable,
)

__all__ = [
    "Awaitable",
    "Coroutine",
    "AsyncIterable",
    "AsyncIterator",
    "AsyncGenerator",
    "Hashable",
    "Iterable",
    "Iterator",
    "Generator",
    "Reversible",
    "Sized",
    "Container",
    "Callable",
    "Collection",
    "Set",
    "MutableSet",
    "Mapping",
    "MutableMapping",
    "MappingView",
    "KeysView",
    "ItemsView",
    "ValuesView",
    "Sequence",
    "MutableSequence",
    "ByteString",
]
if sys.version_info >= (3, 12):
    __all__ += ["Buffer"]

if sys.version_info >= (3, 12):
    @runtime_checkable
    class Buffer(Protocol):
        @abstractmethod
        def __buffer__(self, __flags: int) -> bytes: ...
