import _typeshed
from _typeshed import SupportsWrite
from collections.abc import Callable
from typing import Any, TypeVar

_T = TypeVar("_T")
_FuncT = TypeVar("_FuncT", bound=Callable[..., Any])

# These definitions have special processing in mypy
class ABCMeta(type):
    def __new__(
        __mcls: type[_typeshed.Self], __name: str, __bases: tuple[type, ...], __namespace: dict[str, Any], **kwargs: Any
    ) -> _typeshed.Self: ...
    def __instancecheck__(cls: ABCMeta, instance: Any) -> bool: ...
    def __subclasscheck__(cls: ABCMeta, subclass: type) -> bool: ...
    def _dump_registry(cls: ABCMeta, file: SupportsWrite[str] | None = None) -> None: ...
    def register(cls: ABCMeta, subclass: type[_T]) -> type[_T]: ...

def abstractmethod(funcobj: _FuncT) -> _FuncT: ...

class ABC(metaclass=ABCMeta):
    __slots__ = ()
