"""
Iterators across greenlets or AsyncResult objects.

"""

from collections.abc import Callable, Iterable
from typing import Any, TypeVar
from typing_extensions import ParamSpec, Self

from gevent.greenlet import Greenlet
from gevent.queue import UnboundQueue

_T = TypeVar("_T")
_P = ParamSpec("_P")

# this matches builtins.map to some degree, but since it is an non-public API type that just gets
# returned by some public API functions, we don't bother adding a whole bunch of overloads to handle
# the case of 1-n Iterables being passed in and just go for the fully unsafe signature
# we do the crazy overloads instead in the functions that create these objects
class IMapUnordered(Greenlet[_P, _T]):
    """IMapUnordered(func, iterable, spawn, maxsize=None, _zipped=False)

    At iterator of map results.
    """

    finished: bool
    # it may contain an undocumented Failure object
    queue: UnboundQueue[_T | object]
    def __init__(self, func: Callable[_P, _T], iterable: Iterable[Any], spawn: Callable[_P, Greenlet[_P, _T]]) -> None:
        """
        An iterator that.

        :param callable spawn: The function we use to create new greenlets.
        :keyword int maxsize: If given and not-None, specifies the maximum number of
            finished results that will be allowed to accumulated awaiting the reader;
            more than that number of results will cause map function greenlets to begin
            to block. This is most useful is there is a great disparity in the speed of
            the mapping code and the consumer and the results consume a great deal of resources.
            Using a bound is more computationally expensive than not using a bound.

        .. versionchanged:: 1.1b3
            Added the *maxsize* parameter.
        """

    def __iter__(self) -> Self:
        """Implement iter(self)."""

    def __next__(self) -> _T: ...

class IMap(IMapUnordered[_P, _T]):
    """IMap(*args, **kwargs)"""

    index: int

__all__ = ["IMapUnordered", "IMap"]
