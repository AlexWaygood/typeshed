import abc
import typing
from collections.abc import Buffer as Buffer
from types import GenericAlias, UnionType, get_original_bases as get_original_bases
from typing import (  # noqa: Y022,Y038
    IO as IO,
    TYPE_CHECKING as TYPE_CHECKING,
    AbstractSet as AbstractSet,
    Any as Any,
    AnyStr as AnyStr,
    Callable,
    ClassVar,
    ItemsView,
    KeysView,
    LiteralString as LiteralString,
    Mapping,
    Never as Never,
    NotRequired as NotRequired,
    Required as Required,
    Self as Self,
    TypeAlias as TypeAlias,
    TypeGuard as TypeGuard,
    Unpack as Unpack,
    ValuesView,
    overload,
)

_T = typing.TypeVar("_T")
_F = typing.TypeVar("_F", bound=Callable[..., Any])
_TC = typing.TypeVar("_TC", bound=type[object])

class _SpecialForm:
    def __getitem__(self, parameters: Any) -> object: ...

Protocol: _SpecialForm

def runtime_checkable(cls: _TC) -> _TC: ...

Final: _SpecialForm

def final(f: _F) -> _F: ...

Literal: _SpecialForm

class _TypedDict(Mapping[str, object], metaclass=abc.ABCMeta):
    __total__: ClassVar[bool]
    __orig_bases__: ClassVar[tuple[Any, ...]]
    def copy(self) -> Self: ...
    def setdefault(self, k: Never, default: object) -> object: ...
    def pop(self, k: Never, default: _T = ...) -> object: ...
    def update(self: _T, __m: _T) -> None: ...
    def items(self) -> ItemsView[str, object]: ...
    def keys(self) -> KeysView[str]: ...
    def values(self) -> ValuesView[object]: ...
    def __delitem__(self, k: Never) -> None: ...

TypedDict: object

@overload
def get_origin(tp: UnionType) -> type[UnionType]: ...
@overload
def get_origin(tp: GenericAlias) -> type: ...
@overload
def get_origin(tp: Any) -> Any | None: ...

Annotated: _SpecialForm
