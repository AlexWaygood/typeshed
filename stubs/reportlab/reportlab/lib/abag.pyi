"""Data structure to hold a collection of attributes, used by styles."""

from typing import Any, Final
from typing_extensions import Self

__version__: Final[str]

class ABag:
    """
    'Attribute Bag' - a trivial BAG class for holding attributes.

    This predates modern Python.  Doing this again, we'd use a subclass
    of dict.

    You may initialize with keyword arguments.
    a = ABag(k0=v0,....,kx=vx,....) ==> getattr(a,'kx')==vx

    c = a.clone(ak0=av0,.....) copy with optional additional attributes.
    """

    def __init__(self, **attr: Any) -> None: ...
    def clone(self, **attr: Any) -> Self: ...
    # ABag can have arbitrary attributes
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
