from logging import Logger
from typing import Any, TypeVar, overload

_K = TypeVar("_K")

log: Logger

@overload
def metadata_to_dict(obj: dict[_K, Any]) -> dict[_K, Any]:
    """
    Convert object to dict with all serializable properties like:
    dict, list, set, tuple, str, bool, int, float, type, object, etc.
    """

@overload
def metadata_to_dict(obj: type) -> str: ...
@overload
def metadata_to_dict(obj: Any) -> Any: ...
