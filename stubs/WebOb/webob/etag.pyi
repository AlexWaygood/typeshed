"""
Does parsing of ETag-related headers: If-None-Matches, If-Matches

Also If-Range parsing
"""

from collections.abc import Collection
from datetime import datetime
from typing import Literal
from typing_extensions import TypeAlias

from webob._types import AsymmetricPropertyWithDelete
from webob.response import Response

__all__ = ["AnyETag", "NoETag", "ETagMatcher", "IfRange", "etag_property"]

_ETag: TypeAlias = _AnyETag | _NoETag | ETagMatcher
_ETagProperty: TypeAlias = AsymmetricPropertyWithDelete[_ETag, _ETag | str | None]

def etag_property(key: str, default: _ETag, rfc_section: str, strong: bool = True) -> _ETagProperty: ...

class _AnyETag:
    """
    Represents an ETag of *, or a missing ETag when matching is 'safe'
    """

    def __bool__(self) -> Literal[False]: ...
    def __contains__(self, other: str | None) -> Literal[True]: ...

AnyETag: _AnyETag

class _NoETag:
    """
    Represents a missing ETag when matching is unsafe
    """

    def __bool__(self) -> Literal[False]: ...
    def __contains__(self, other: str | None) -> Literal[False]: ...

NoETag: _NoETag

class ETagMatcher:
    etags: Collection[str]
    def __init__(self, etags: Collection[str]) -> None: ...
    def __contains__(self, other: str | None) -> bool: ...
    @classmethod
    def parse(cls, value: str, strong: bool = True) -> ETagMatcher | _AnyETag:
        """
        Parse this from a header value
        """

class IfRange:
    etag: _ETag
    def __init__(self, etag: _ETag) -> None: ...
    @classmethod
    def parse(cls, value: str | None) -> IfRange | IfRangeDate:
        """
        Parse this from a header value.
        """

    def __contains__(self, resp: Response) -> bool:
        """
        Return True if the If-Range header matches the given etag or last_modified
        """

    def __bool__(self) -> bool: ...

class IfRangeDate:
    date: datetime
    def __init__(self, date: datetime) -> None: ...
    def __contains__(self, resp: Response) -> bool: ...
