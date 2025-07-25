from typing import Any
from typing_extensions import Self

class ExceptionCauseMixin(Exception):
    """
    A mixin class for wrapping an exception in another exception, or
    otherwise indicating an exception was caused by another exception.

    This is most useful in concurrent or failure-intolerant scenarios,
    where just because one operation failed, doesn't mean the remainder
    should be aborted, or that it's the appropriate time to raise
    exceptions.

    This is still a work in progress, but an example use case at the
    bottom of this module.

    NOTE: when inheriting, you will probably want to put the
    ExceptionCauseMixin first. Builtin exceptions are not good about
    calling super()
    """

    cause: Any
    def __new__(cls, *args, **kw) -> Self: ...
    def get_str(self) -> str:
        """
        Get formatted the formatted traceback and exception
        message. This function exists separately from __str__()
        because __str__() is somewhat specialized for the built-in
        traceback module's particular usage.
        """

class MathError(ExceptionCauseMixin, ValueError): ...

__all__ = ["ExceptionCauseMixin"]
