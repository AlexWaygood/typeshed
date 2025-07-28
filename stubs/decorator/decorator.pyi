"""
Decorator module, see
https://github.com/micheles/decorator/blob/master/docs/documentation.md
for the documentation.
"""

import inspect
from builtins import dict as _dict  # alias to avoid conflicts with attribute name
from collections.abc import Callable, Generator, Iterator
from contextlib import _GeneratorContextManager
from inspect import Signature, getfullargspec as getfullargspec, iscoroutinefunction as iscoroutinefunction
from re import Pattern
from typing import Any, Final, Literal, TypeVar
from typing_extensions import ParamSpec

_C = TypeVar("_C", bound=Callable[..., Any])
_Func = TypeVar("_Func", bound=Callable[..., Any])
_T = TypeVar("_T")
_P = ParamSpec("_P")

DEF: Final[Pattern[str]]
POS: Final[Literal[inspect._ParameterKind.POSITIONAL_OR_KEYWORD]]
EMPTY: Final[type[inspect._empty]]

class FunctionMaker:
    """
    An object with the ability to create functions with a given signature.
    It has attributes name, doc, module, signature, defaults, dict and
    methods update and make.
    """

    args: list[str]
    varargs: str | None
    varkw: str | None
    defaults: tuple[Any, ...]
    kwonlyargs: list[str]
    kwonlydefaults: str | None
    shortsignature: str | None
    name: str
    doc: str | None
    module: str | None
    annotations: _dict[str, Any]
    signature: str
    dict: _dict[str, Any]
    def __init__(
        self,
        func: Callable[..., Any] | None = ...,
        name: str | None = ...,
        signature: str | None = ...,
        defaults: tuple[Any, ...] | None = ...,
        doc: str | None = ...,
        module: str | None = ...,
        funcdict: _dict[str, Any] | None = ...,
    ) -> None: ...
    def update(self, func: Any, **kw: Any) -> None:
        """
        Update the signature of func with the data in self
        """

    def make(
        self, src_templ: str, evaldict: _dict[str, Any] | None = ..., addsource: bool = ..., **attrs: Any
    ) -> Callable[..., Any]:
        """
        Make a new function from a given template and update the signature
        """

    @classmethod
    def create(
        cls,
        obj: Any,
        body: str,
        evaldict: _dict[str, Any],
        defaults: tuple[Any, ...] | None = ...,
        doc: str | None = ...,
        module: str | None = ...,
        addsource: bool = ...,
        **attrs: Any,
    ) -> Callable[..., Any]:
        """
        Create a function from the strings name, signature and body.
        evaldict is the evaluation dictionary. If addsource is true an
        attribute __source__ is added to the result. The attributes attrs
        are added, if any.
        """

def fix(args: tuple[Any, ...], kwargs: dict[str, Any], sig: Signature) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """
    Fix args and kwargs to be consistent with the signature
    """

def decorate(func: _Func, caller: Callable[..., Any], extras: tuple[Any, ...] = ..., kwsyntax: bool = False) -> _Func:
    """
    Decorates a function/generator/coroutine using a caller.
    If kwsyntax is True calling the decorated functions with keyword
    syntax will pass the named arguments inside the ``kw`` dictionary,
    even if such argument are positional, similarly to what functools.wraps
    does. By default kwsyntax is False and the the arguments are untouched.
    """

def decoratorx(caller: Callable[..., Any]) -> Callable[..., Any]:
    """
    A version of "decorator" implemented via "exec" and not via the
    Signature object. Use this if you are want to preserve the `.__code__`
    object properties (https://github.com/micheles/decorator/issues/129).
    """

def decorator(
    caller: Callable[..., Any], _func: Callable[..., Any] | None = None, kwsyntax: bool = False
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    decorator(caller) converts a caller function into a decorator
    """

class ContextManager(_GeneratorContextManager[_T]):
    def __init__(self, g: Callable[..., Generator[_T]], *a: Any, **k: Any) -> None: ...
    def __call__(self, func: _C) -> _C: ...

def contextmanager(func: Callable[_P, Iterator[_T]]) -> Callable[_P, ContextManager[_T]]: ...
def append(a: type, vancestors: list[type]) -> None:
    """
    Append ``a`` to the list of the virtual ancestors, unless it is already
    included.
    """

def dispatch_on(*dispatch_args: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Factory of decorators turning a function into a generic function
    dispatching on the given arguments.
    """
