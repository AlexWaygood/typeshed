from typing import Any, final
from weakref import ref

@final
class ValuedWeakRef(ref):
    """
    A weak ref with an associated value.
    """

    value: Any

@final
class IdentRegistry:
    """IdentRegistry()

    Maintains a unique mapping of (small) non-negative integer identifiers
    to objects that can be weakly referenced.

    It is guaranteed that no two objects will have the the same
    identifier at the same time, as long as those objects are
    also uniquely hashable.
    """

    def __init__(self) -> None: ...
    def get_ident(self, obj: object) -> int:
        """IdentRegistry.get_ident(self, obj)

        Retrieve the identifier for *obj*, creating one
        if necessary.
        """

    def __len__(self) -> int:
        """Return len(self)."""

__all__ = ["IdentRegistry"]
