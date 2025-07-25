from collections.abc import Iterator
from typing import overload
from typing_extensions import Self

__all__ = ["Range", "ContentRange"]

class Range:
    """
    Represents the Range header.
    """

    start: int | None
    end: int | None
    @overload
    def __init__(self, start: None, end: None) -> None: ...
    @overload
    def __init__(self, start: int, end: int | None) -> None: ...
    def range_for_length(self, length: int | None) -> tuple[int, int] | None:
        """
        *If* there is only one range, and *if* it is satisfiable by
        the given length, then return a (start, end) non-inclusive range
        of bytes to serve.  Otherwise return None
        """

    def content_range(self, length: int | None) -> ContentRange | None:
        """
        Works like range_for_length; returns None or a ContentRange object

        You can use it like::

            response.content_range = req.range.content_range(response.content_length)

        Though it's still up to you to actually serve that content range!
        """

    def __iter__(self) -> Iterator[int | None]: ...
    @classmethod
    def parse(cls, header: str | None) -> Self | None:
        """
        Parse the header; may return None if header is invalid
        """

class ContentRange:
    """
    Represents the Content-Range header

    This header is ``start-stop/length``, where start-stop and length
    can be ``*`` (represented as None in the attributes).
    """

    start: int | None
    stop: int | None
    length: int | None
    @overload
    def __init__(self, start: None, stop: None, length: int | None) -> None: ...
    @overload
    def __init__(self, start: int, stop: int, length: int | None) -> None: ...
    def __iter__(self) -> Iterator[int | None]:
        """
        Mostly so you can unpack this, like:

            start, stop, length = res.content_range
        """

    @classmethod
    def parse(cls, value: str | None) -> Self | None:
        """
        Parse the header.  May return None if it cannot parse.
        """
