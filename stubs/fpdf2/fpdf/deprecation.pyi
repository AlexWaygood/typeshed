"""
Utilities to manage deprecation errors & warnings.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from types import ModuleType
from typing import Any, NoReturn

def support_deprecated_txt_arg(fn):
    """Decorator converting `txt=` arguments into `text=` arguments"""

class WarnOnDeprecatedModuleAttributes(ModuleType):
    def __call__(self) -> NoReturn: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...

def get_stack_level() -> int:
    """Get the first place in the call stack that is not inside fpdf2"""
