"""
passlib.utils.decor -- helper decorators & properties
"""

from typing import Any

class classproperty:
    """Function decorator which acts like a combination of classmethod+property (limited to read-only properties)"""

    im_func: Any
    def __init__(self, func) -> None: ...
    def __get__(self, obj, cls): ...
    @property
    def __func__(self):
        """py3 compatible alias"""

class hybrid_method:
    """
    decorator which invokes function with class if called as class method,
    and with object if called at instance level.
    """

    func: Any
    def __init__(self, func) -> None: ...
    def __get__(self, obj, cls): ...

def memoize_single_value(func):
    """
    decorator for function which takes no args,
    and memoizes result.  exposes a ``.clear_cache`` method
    to clear the cached value.
    """

class memoized_property:
    """
    decorator which invokes method once, then replaces attr with result
    """

    __func__: Any
    __name__: Any
    __doc__: Any
    def __init__(self, func) -> None: ...
    def __get__(self, obj, cls): ...
    def clear_cache(self, obj) -> None:
        """
        class-level helper to clear stored value (if any).

        usage: :samp:`type(self).{attr}.clear_cache(self)`
        """

    def peek_cache(self, obj, default=None):
        """
        class-level helper to peek at stored value

        usage: :samp:`value = type(self).{attr}.clear_cache(self)`
        """

def deprecated_function(
    msg=None, deprecated=None, removed=None, updoc: bool = True, replacement=None, _is_method: bool = False, func_module=None
):
    """decorator to deprecate a function.

    :arg msg: optional msg, default chosen if omitted
    :kwd deprecated: version when function was first deprecated
    :kwd removed: version when function will be removed
    :kwd replacement: alternate name / instructions for replacing this function.
    :kwd updoc: add notice to docstring (default ``True``)
    """

def deprecated_method(msg=None, deprecated=None, removed=None, updoc: bool = True, replacement=None):
    """decorator to deprecate a method.

    :arg msg: optional msg, default chosen if omitted
    :kwd deprecated: version when method was first deprecated
    :kwd removed: version when method will be removed
    :kwd replacement: alternate name / instructions for replacing this method.
    :kwd updoc: add notice to docstring (default ``True``)
    """

__all__ = [
    "classproperty",
    "hybrid_method",
    "memoize_single_value",
    "memoized_property",
    "deprecated_function",
    "deprecated_method",
]
