"""
requests.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power Requests.
"""

from collections.abc import Iterable, Iterator, Mapping, MutableMapping
from typing import Any, Generic, TypeVar, overload

_D = TypeVar("_D")
_VT = TypeVar("_VT")

class CaseInsensitiveDict(MutableMapping[str, _VT], Generic[_VT]):
    """A case-insensitive ``dict``-like object.

    Implements all methods and operations of
    ``MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive::

        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.
    """

    def __init__(self, data: Mapping[str, _VT] | Iterable[tuple[str, _VT]] | None = None, **kwargs: _VT) -> None: ...
    def lower_items(self) -> Iterator[tuple[str, _VT]]:
        """Like iteritems(), but with all lowercase keys."""

    def __setitem__(self, key: str, value: _VT) -> None: ...
    def __getitem__(self, key: str) -> _VT: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def copy(self) -> CaseInsensitiveDict[_VT]: ...

class LookupDict(dict[str, _VT]):
    """Dictionary lookup object."""

    name: Any
    def __init__(self, name: Any = None) -> None: ...
    def __getitem__(self, key: str) -> _VT | None: ...  # type: ignore[override]
    def __setattr__(self, attr: str, value: _VT, /) -> None: ...
    @overload
    def get(self, key: str, default: None = None) -> _VT | None: ...
    @overload
    def get(self, key: str, default: _D | _VT) -> _D | _VT: ...
