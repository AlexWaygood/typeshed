from collections import defaultdict
from typing import TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

class BoundDictionary(defaultdict[_KT, _VT]):
    """
    A default dictionary where elements are tightly coupled.

    The factory method is responsible for binding the parent object to the child.

    If a reference attribute is assigned then child objects will have the key assigned to this.

    Otherwise it's just a defaultdict.
    """

    reference: str | None
    def __init__(self, reference: str | None = None, *args, **kw) -> None: ...
