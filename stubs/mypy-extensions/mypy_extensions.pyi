"""Defines experimental extensions to the standard "typing" module that are
supported by the mypy typechecker.

Example usage:
    from mypy_extensions import TypedDict
"""

import abc
from _collections_abc import dict_items, dict_keys, dict_values
from _typeshed import IdentityFunction, Unused
from collections.abc import Mapping
from typing import Any, ClassVar, Generic, TypeVar, overload, type_check_only
from typing_extensions import Never, Self, deprecated

_T = TypeVar("_T")
_U = TypeVar("_U")

# Internal mypy fallback type for all typed dicts (does not exist at runtime)
# N.B. Keep this mostly in sync with typing(_extensions)._TypedDict
@type_check_only
@deprecated("Use typing._TypedDict instead")
class _TypedDict(Mapping[str, object], metaclass=abc.ABCMeta):
    __total__: ClassVar[bool]
    # Unlike typing(_extensions).TypedDict,
    # subclasses of mypy_extensions.TypedDict do NOT have the __required_keys__ and __optional_keys__ ClassVars
    def copy(self) -> Self: ...
    # Using Never so that only calls using mypy plugin hook that specialize the signature
    # can go through.
    def setdefault(self, k: Never, default: object) -> object: ...
    # Mypy plugin hook for 'pop' expects that 'default' has a type variable type.
    def pop(self, k: Never, default: _T = ...) -> object: ...  # pyright: ignore[reportInvalidTypeVarUse]
    def update(self, m: Self, /) -> None: ...
    def items(self) -> dict_items[str, object]: ...
    def keys(self) -> dict_keys[str, object]: ...
    def values(self) -> dict_values[str, object]: ...
    def __delitem__(self, k: Never) -> None: ...
    @overload
    def __or__(self, value: Self, /) -> Self: ...
    @overload
    def __or__(self, value: dict[str, Any], /) -> dict[str, object]: ...
    @overload
    def __ror__(self, value: Self, /) -> Self: ...
    @overload
    def __ror__(self, value: dict[str, Any], /) -> dict[str, object]: ...
    # supposedly incompatible definitions of `__or__` and `__ior__`:
    def __ior__(self, value: Self, /) -> Self: ...  # type: ignore[misc]

@deprecated("Use typing.TypedDict or typing_extensions.TypedDict instead")
def TypedDict(typename: str, fields: dict[str, type[Any]], total: bool = ...) -> type[dict[str, Any]]:
    """A simple typed name space. At runtime it is equivalent to a plain dict.

    TypedDict creates a dictionary type that expects all of its
    instances to have a certain set of keys, with each key
    associated with a value of a consistent type. This expectation
    is not checked at runtime but is only enforced by typecheckers.
    Usage::

        Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': str})
        a: Point2D = {'x': 1, 'y': 2, 'label': 'good'}  # OK
        b: Point2D = {'z': 3, 'label': 'bad'}           # Fails type check
        assert Point2D(x=1, y=2, label='first') == dict(x=1, y=2, label='first')

    The type info could be accessed via Point2D.__annotations__. TypedDict
    supports two additional equivalent forms::

        Point2D = TypedDict('Point2D', x=int, y=int, label=str)

        class Point2D(TypedDict):
            x: int
            y: int
            label: str

    The latter syntax is only supported in Python 3.6+, while two other
    syntax forms work for 3.2+
    """

@overload
def Arg(type: _T, name: str | None = ...) -> _T:
    """A normal positional argument"""

@overload
def Arg(*, name: str | None = ...) -> Any: ...
@overload
def DefaultArg(type: _T, name: str | None = ...) -> _T:
    """A positional argument with a default value"""

@overload
def DefaultArg(*, name: str | None = ...) -> Any: ...
@overload
def NamedArg(type: _T, name: str | None = ...) -> _T:
    """A keyword-only argument"""

@overload
def NamedArg(*, name: str | None = ...) -> Any: ...
@overload
def DefaultNamedArg(type: _T, name: str | None = ...) -> _T:
    """A keyword-only argument with a default value"""

@overload
def DefaultNamedArg(*, name: str | None = ...) -> Any: ...
@overload
def VarArg(type: _T) -> _T:
    """A *args-style variadic positional argument"""

@overload
def VarArg() -> Any: ...
@overload
def KwArg(type: _T) -> _T:
    """A **kwargs-style variadic keyword argument"""

@overload
def KwArg() -> Any: ...

# Return type that indicates a function does not return.
# Deprecated: Use typing.NoReturn instead.
@deprecated("Use typing.NoReturn or typing.Never instead")
class NoReturn: ...

# This is consistent with implementation. Usage intends for this as
# a class decorator, but mypy does not support type[_T] for abstract
# classes until this issue is resolved, https://github.com/python/mypy/issues/4717.
def trait(cls: _T) -> _T: ...
def mypyc_attr(*attrs: str, **kwattrs: Unused) -> IdentityFunction: ...

class FlexibleAlias(Generic[_T, _U]): ...

# Mypy and mypyc treat these native int types as different from 'int', but this is
# a non-standard extension. For other tools, aliasing these to 'int' allows them
# to mostly do the right thing with these types.
i64 = int
i32 = int
i16 = int
u8 = int
