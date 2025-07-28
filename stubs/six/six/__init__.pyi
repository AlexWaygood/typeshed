"""Utilities for writing code that runs on Python 2 and 3"""

import builtins
import operator
import types
import unittest
from _typeshed import IdentityFunction, SupportsGetItem, Unused
from builtins import next as next
from collections.abc import Callable, ItemsView, Iterable, Iterator as _Iterator, KeysView, Mapping, ValuesView
from functools import wraps as wraps
from importlib.util import spec_from_loader as spec_from_loader
from io import BytesIO as BytesIO, StringIO as StringIO
from re import Pattern
from typing import Any, AnyStr, Literal, NoReturn, TypeVar, overload

from six import moves as moves

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")

__author__: str
__version__: str

PY2: Literal[False]
PY3: Literal[True]
PY34: Literal[True]

string_types: tuple[type[str]]
integer_types: tuple[type[int]]
class_types: tuple[type[type]]
text_type = str
binary_type = bytes

MAXSIZE: int

callable = builtins.callable

def get_unbound_function(unbound: types.FunctionType) -> types.FunctionType:
    """Get the function out of a possibly unbound function"""

create_bound_method = types.MethodType

def create_unbound_method(func: types.FunctionType, cls: type) -> types.FunctionType: ...

Iterator = object

def get_method_function(meth: types.MethodType) -> types.FunctionType:
    """Return a callable object that fetches the given attribute(s) from its operand.
    After f = attrgetter('name'), the call f(r) returns r.name.
    After g = attrgetter('name', 'date'), the call g(r) returns (r.name, r.date).
    After h = attrgetter('name.first', 'name.last'), the call h(r) returns
    (r.name.first, r.name.last).
    """

def get_method_self(meth: types.MethodType) -> object:
    """Return a callable object that fetches the given attribute(s) from its operand.
    After f = attrgetter('name'), the call f(r) returns r.name.
    After g = attrgetter('name', 'date'), the call g(r) returns (r.name, r.date).
    After h = attrgetter('name.first', 'name.last'), the call h(r) returns
    (r.name.first, r.name.last).
    """

def get_function_closure(fun: types.FunctionType) -> tuple[types.CellType, ...] | None:
    """Return a callable object that fetches the given attribute(s) from its operand.
    After f = attrgetter('name'), the call f(r) returns r.name.
    After g = attrgetter('name', 'date'), the call g(r) returns (r.name, r.date).
    After h = attrgetter('name.first', 'name.last'), the call h(r) returns
    (r.name.first, r.name.last).
    """

def get_function_code(fun: types.FunctionType) -> types.CodeType:
    """Return a callable object that fetches the given attribute(s) from its operand.
    After f = attrgetter('name'), the call f(r) returns r.name.
    After g = attrgetter('name', 'date'), the call g(r) returns (r.name, r.date).
    After h = attrgetter('name.first', 'name.last'), the call h(r) returns
    (r.name.first, r.name.last).
    """

def get_function_defaults(fun: types.FunctionType) -> tuple[Any, ...] | None:
    """Return a callable object that fetches the given attribute(s) from its operand.
    After f = attrgetter('name'), the call f(r) returns r.name.
    After g = attrgetter('name', 'date'), the call g(r) returns (r.name, r.date).
    After h = attrgetter('name.first', 'name.last'), the call h(r) returns
    (r.name.first, r.name.last).
    """

def get_function_globals(fun: types.FunctionType) -> dict[str, Any]:
    """Return a callable object that fetches the given attribute(s) from its operand.
    After f = attrgetter('name'), the call f(r) returns r.name.
    After g = attrgetter('name', 'date'), the call g(r) returns (r.name, r.date).
    After h = attrgetter('name.first', 'name.last'), the call h(r) returns
    (r.name.first, r.name.last).
    """

def iterkeys(d: Mapping[_K, Any]) -> _Iterator[_K]:
    """Return an iterator over the keys of a dictionary."""

def itervalues(d: Mapping[Any, _V]) -> _Iterator[_V]:
    """Return an iterator over the values of a dictionary."""

def iteritems(d: Mapping[_K, _V]) -> _Iterator[tuple[_K, _V]]:
    """Return an iterator over the (key, value) pairs of a dictionary."""

def viewkeys(d: Mapping[_K, Any]) -> KeysView[_K]:
    """Return a callable object that calls the given method on its operand.
    After f = methodcaller('name'), the call f(r) returns r.name().
    After g = methodcaller('name', 'date', foo=1), the call g(r) returns
    r.name('date', foo=1).
    """

def viewvalues(d: Mapping[Any, _V]) -> ValuesView[_V]:
    """Return a callable object that calls the given method on its operand.
    After f = methodcaller('name'), the call f(r) returns r.name().
    After g = methodcaller('name', 'date', foo=1), the call g(r) returns
    r.name('date', foo=1).
    """

def viewitems(d: Mapping[_K, _V]) -> ItemsView[_K, _V]:
    """Return a callable object that calls the given method on its operand.
    After f = methodcaller('name'), the call f(r) returns r.name().
    After g = methodcaller('name', 'date', foo=1), the call g(r) returns
    r.name('date', foo=1).
    """

def b(s: str) -> bytes:
    """Byte literal"""

def u(s: str) -> str:
    """Text literal"""

unichr = chr

def int2byte(i: int) -> bytes:
    """S.pack(v1, v2, ...) -> bytes

    Return a bytes object containing values v1, v2, ... packed according
    to the format string S.format.  See help(struct) for more on format
    strings.
    """

# Should be `byte2int: operator.itemgetter[int]`. But a bug in mypy prevents using TypeVar in itemgetter.__call__
def byte2int(obj: SupportsGetItem[int, _T]) -> _T:
    """Return a callable object that fetches the given item(s) from its operand.
    After f = itemgetter(2), the call f(r) returns r[2].
    After g = itemgetter(2, 5, 3), the call g(r) returns (r[2], r[5], r[3])
    """

indexbytes = operator.getitem
iterbytes = iter

def assertCountEqual(self: unittest.TestCase, first: Iterable[_T], second: Iterable[_T], msg: str | None = ...) -> None: ...
@overload
def assertRaisesRegex(self: unittest.TestCase, msg: str | None = ...) -> Any: ...
@overload
def assertRaisesRegex(self: unittest.TestCase, callable_obj: Callable[..., object], *args: Any, **kwargs: Any) -> Any: ...
def assertRegex(self: unittest.TestCase, text: AnyStr, expected_regex: AnyStr | Pattern[AnyStr], msg: Any = ...) -> None: ...
def assertNotRegex(self: unittest.TestCase, text: AnyStr, expected_regex: AnyStr | Pattern[AnyStr], msg: Any = ...) -> None: ...

exec_ = exec

def reraise(tp: type[BaseException] | None, value: BaseException | None, tb: types.TracebackType | None = None) -> NoReturn:
    """Reraise an exception."""

def raise_from(value: BaseException | type[BaseException], from_value: BaseException | None) -> NoReturn: ...

print_ = print

def with_metaclass(meta: type, *bases: type) -> type:
    """Create a base class with a metaclass."""

def add_metaclass(metaclass: type) -> IdentityFunction:
    """Class decorator for creating a class with a metaclass."""

def ensure_binary(s: bytes | str, encoding: str = "utf-8", errors: str = "strict") -> bytes:
    """Coerce **s** to six.binary_type.

    For Python 2:
      - `unicode` -> encoded to `str`
      - `str` -> `str`

    For Python 3:
      - `str` -> encoded to `bytes`
      - `bytes` -> `bytes`
    """

def ensure_str(s: bytes | str, encoding: str = "utf-8", errors: str = "strict") -> str:
    """Coerce *s* to `str`.

    For Python 2:
      - `unicode` -> encoded to `str`
      - `str` -> `str`

    For Python 3:
      - `str` -> `str`
      - `bytes` -> decoded to `str`
    """

def ensure_text(s: bytes | str, encoding: str = "utf-8", errors: str = "strict") -> str:
    """Coerce *s* to six.text_type.

    For Python 2:
      - `unicode` -> `unicode`
      - `str` -> `unicode`

    For Python 3:
      - `str` -> `str`
      - `bytes` -> decoded to `str`
    """

def python_2_unicode_compatible(klass: _T) -> _T:
    """
    A class decorator that defines __unicode__ and __str__ methods under Python 2.
    Under Python 3 it does nothing.

    To support Python 2 and 3 with a single code base, define a __str__ method
    returning text and apply this decorator to the class.
    """

class _LazyDescr:
    name: str
    def __init__(self, name: str) -> None: ...
    def __get__(self, obj: object, tp: Unused) -> Any: ...

class MovedModule(_LazyDescr):
    mod: str
    def __init__(self, name: str, old: str, new: str | None = None) -> None: ...
    def __getattr__(self, attr: str) -> Any: ...

class MovedAttribute(_LazyDescr):
    mod: str
    attr: str
    def __init__(
        self, name: str, old_mod: str, new_mod: str, old_attr: str | None = None, new_attr: str | None = None
    ) -> None: ...

def add_move(move: MovedModule | MovedAttribute) -> None:
    """Add an item to six.moves."""

def remove_move(name: str) -> None:
    """Remove item from six.moves."""

advance_iterator = next
