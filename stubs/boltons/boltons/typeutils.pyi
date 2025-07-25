"""Python's built-in :mod:`functools` module builds several useful
utilities on top of Python's first-class function support.
``typeutils`` attempts to do the same for metaprogramming with types
and instances.
"""

from typing import Any, Literal, Protocol
from typing_extensions import Self

class _Sentinel(Protocol):
    def __bool__(self) -> Literal[False]: ...
    def __copy__(self) -> Self: ...
    def __deepcopy__(self, _memo) -> Self: ...

def make_sentinel(name: str = "_MISSING", var_name: str | None = None) -> _Sentinel:
    """Creates and returns a new **instance** of a new class, suitable for
    usage as a "sentinel", a kind of singleton often used to indicate
    a value is missing when ``None`` is a valid input.

    Args:
        name (str): Name of the Sentinel
        var_name (str): Set this name to the name of the variable in
            its respective module enable pickleability. Note:
            pickleable sentinels should be global constants at the top
            level of their module.

    >>> make_sentinel(var_name='_MISSING')
    _MISSING

    The most common use cases here in boltons are as default values
    for optional function arguments, partly because of its
    less-confusing appearance in automatically generated
    documentation. Sentinels also function well as placeholders in queues
    and linked lists.

    .. note::

      By design, additional calls to ``make_sentinel`` with the same
      values will not produce equivalent objects.

      >>> make_sentinel('TEST') == make_sentinel('TEST')
      False
      >>> type(make_sentinel('TEST')) == type(make_sentinel('TEST'))
      False

    """

def issubclass(subclass: type, baseclass: type) -> bool:
    """Just like the built-in :func:`issubclass`, this function checks
    whether *subclass* is inherited from *baseclass*. Unlike the
    built-in function, this ``issubclass`` will simply return
    ``False`` if either argument is not suitable (e.g., if *subclass*
    is not an instance of :class:`type`), instead of raising
    :exc:`TypeError`.

    Args:
        subclass (type): The target class to check.
        baseclass (type): The base class *subclass* will be checked against.

    >>> class MyObject(object): pass
    ...
    >>> issubclass(MyObject, object)  # always a fun fact
    True
    >>> issubclass('hi', 'friend')
    False
    """

def get_all_subclasses(cls: type) -> list[type]:
    """Recursively finds and returns a :class:`list` of all types
    inherited from *cls*.

    >>> class A(object):
    ...     pass
    ...
    >>> class B(A):
    ...     pass
    ...
    >>> class C(B):
    ...     pass
    ...
    >>> class D(A):
    ...     pass
    ...
    >>> [t.__name__ for t in get_all_subclasses(A)]
    ['B', 'D', 'C']
    >>> [t.__name__ for t in get_all_subclasses(B)]
    ['C']

    """

class classproperty:
    """Much like a :class:`property`, but the wrapped get function is a
    class method.  For simplicity, only read-only properties are
    implemented.
    """

    fn: Any
    def __init__(self, fn) -> None: ...
    def __get__(self, instance, cls): ...
