from collections.abc import Mapping, Sequence
from importlib.abc import Loader
from types import ModuleType

# Signature of `builtins.__import__` should be kept identical to `importlib.__import__`
def __import__(
    name: str,
    globals: Mapping[str, object] | None = None,
    locals: Mapping[str, object] | None = None,
    fromlist: Sequence[str] = (),
    level: int = 0,
) -> ModuleType: ...
def find_loader(name: str, path: str | None = None) -> Loader | None: ...
