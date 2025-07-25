from collections.abc import Iterator
from typing import Generic, TypeVar
from typing_extensions import Self

_T_co = TypeVar("_T_co", covariant=True)

class CancellableStream(Generic[_T_co]):
    """
    Stream wrapper for real-time events, logs, etc. from the server.

    Example:
        >>> events = client.events()
        >>> for event in events:
        ...   print(event)
        >>> # and cancel from another thread
        >>> events.close()
    """

    def __init__(self, stream: Iterator[_T_co], response) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> _T_co: ...
    next = __next__
    def close(self) -> None:
        """
        Closes the event streaming.
        """
