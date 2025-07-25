from collections.abc import ItemsView, Mapping, MutableMapping
from typing import Any, TypeVar

_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)
_MM = TypeVar("_MM", bound=MutableMapping[Any, Any])

def url_join(base: str, *args: str) -> str:
    """
    Helper function to join an arbitrary number of url segments together.
    """

def copy_kwargs(dictionary: _MM) -> _MM: ...
def iterator(d: Mapping[_KT, _VT_co]) -> ItemsView[_KT, _VT_co]:
    """
    Helper to get and a proper dict iterator with Py2k and Py3k
    """
