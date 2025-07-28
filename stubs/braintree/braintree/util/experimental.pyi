from typing import TypeVar

_T = TypeVar("_T")

def Experimental(cls: _T) -> _T:
    """
    Experimental features may change at any time.

    Decorator to mark a class as experimental.
    Adds an '_is_experimental' attribute to the class.
    """
