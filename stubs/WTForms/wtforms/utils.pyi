from collections.abc import Iterable, Iterator
from typing import Any, Literal

from wtforms.meta import _MultiDictLikeWithGetall

def clean_datetime_format_for_strptime(formats: Iterable[str]) -> list[str]:
    """
    Remove dashes used to disable zero-padding with strftime formats (for
    compatibility with strptime).
    """

class UnsetValue:
    """
    An unset value.

    This is used in situations where a blank value like `None` is acceptable
    usually as the default value of a class variable or function parameter
    (iow, usually when `None` is a valid value.)
    """

    def __bool__(self) -> Literal[False]: ...

unset_value: UnsetValue

class WebobInputWrapper:
    """
    Wrap a webob MultiDict for use as passing as `formdata` to Field.

    Since for consistency, we have decided in WTForms to support as input a
    small subset of the API provided in common between cgi.FieldStorage,
    Django's QueryDict, and Werkzeug's MultiDict, we need to wrap Webob, the
    only supported framework whose multidict does not fit this API, but is
    nevertheless used by a lot of frameworks.

    While we could write a full wrapper to support all the methods, this will
    undoubtedly result in bugs due to some subtle differences between the
    various wrappers. So we will keep it simple.
    """

    def __init__(self, multidict: _MultiDictLikeWithGetall) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, name: str) -> bool: ...
    def getlist(self, name: str) -> list[Any]: ...
