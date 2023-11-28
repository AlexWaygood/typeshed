from typing import Any, Callable, TypeVar

_FuncT = TypeVar("_FuncT", bound=Callable[..., Any])

class ABCMeta(type): ...

def abstractmethod(funcobj: _FuncT) -> _FuncT: ...
