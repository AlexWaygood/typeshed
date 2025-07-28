"""Error formatting function for Windows.

The code is taken from twisted.python.win32 module.
"""

from collections.abc import Callable

formatError: Callable[[object], str]

__all__ = ["formatError"]
