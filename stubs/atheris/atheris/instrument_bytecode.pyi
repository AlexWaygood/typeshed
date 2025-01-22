from collections.abc import Callable
from typing import TypeVar

_T = TypeVar("_T")

def instrument_func[_T](func: Callable[..., _T]) -> Callable[..., _T]: ...
def instrument_all() -> None: ...
