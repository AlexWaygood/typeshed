"""
Monkey patching of distutils.
"""

from types import FunctionType
from typing import TypeVar, overload

_T = TypeVar("_T")
_UnpatchT = TypeVar("_UnpatchT", type, FunctionType)
__all__: list[str] = []

@overload
def get_unpatched(item: _UnpatchT) -> _UnpatchT: ...  # type: ignore[overload-overlap]
@overload
def get_unpatched(item: object) -> None: ...
def get_unpatched_class(cls: type[_T]) -> type[_T]:
    """Protect against re-patching the distutils if reloaded

    Also ensures that no other distutils extension monkeypatched the distutils
    first.
    """

def patch_all() -> None: ...
def patch_func(replacement, target_mod, func_name) -> None:
    """
    Patch func_name in target_mod with replacement

    Important - original must be resolved by name to avoid
    patching an already patched function.
    """

def get_unpatched_function(candidate): ...
