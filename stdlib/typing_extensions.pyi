import abc
import typing
from collections.abc import Buffer as Buffer
from types import GenericAlias, UnionType, get_original_bases as get_original_bases
from typing import (  # noqa: Y022,Y037,Y038
    IO as IO,
    TYPE_CHECKING as TYPE_CHECKING,
    AbstractSet as AbstractSet,
    Any as Any,
    AnyStr as AnyStr,
    AsyncGenerator as AsyncGenerator,
    AsyncIterable as AsyncIterable,
    AsyncIterator as AsyncIterator,
    Awaitable as Awaitable,
    BinaryIO as BinaryIO,
    Callable as Callable,
    ClassVar as ClassVar,
    Collection as Collection,
    Concatenate as Concatenate,
    Container as Container,
    Coroutine as Coroutine,
    Dict as Dict,
    ForwardRef as ForwardRef,
    Generator as Generator,
    Generic as Generic,
    Hashable as Hashable,
    ItemsView as ItemsView,
    Iterable as Iterable,
    Iterator as Iterator,
    KeysView as KeysView,
    List as List,
    LiteralString as LiteralString,
    Mapping as Mapping,
    MappingView as MappingView,
    MutableMapping as MutableMapping,
    MutableSequence as MutableSequence,
    MutableSet as MutableSet,
    NamedTuple as NamedTuple,
    Never as Never,
    NewType as NewType,
    NoReturn as NoReturn,
    NotRequired as NotRequired,
    Optional as Optional,
    Required as Required,
    Reversible as Reversible,
    Self as Self,
    Sequence as Sequence,
    Set as Set,
    Sized as Sized,
    SupportsAbs as SupportsAbs,
    SupportsBytes as SupportsBytes,
    SupportsFloat as SupportsFloat,
    SupportsInt as SupportsInt,
    SupportsRound as SupportsRound,
    TextIO as TextIO,
    Tuple as Tuple,
    Type as Type,
    TypeAlias as TypeAlias,
    TypeGuard as TypeGuard,
    Union as Union,
    Unpack as Unpack,
    ValuesView as ValuesView,
    _Alias,
    cast as cast,
    overload as overload,
    type_check_only,
)

_T = typing.TypeVar("_T")
_F = typing.TypeVar("_F", bound=Callable[..., Any])
_TC = typing.TypeVar("_TC", bound=type[object])

# unfortunately we have to duplicate this class definition from typing.pyi or we break pytype
class _SpecialForm:
    def __getitem__(self, parameters: Any) -> object: ...

# Do not import (and re-export) Protocol or runtime_checkable from
# typing module because type checkers need to be able to distinguish
# typing.Protocol and typing_extensions.Protocol so they can properly
# warn users about potential runtime exceptions when using typing.Protocol
# on older versions of Python.
Protocol: _SpecialForm

def runtime_checkable(cls: _TC) -> _TC: ...

# This alias for above is kept here for backwards compatibility.
runtime = runtime_checkable
Final: _SpecialForm

def final(f: _F) -> _F: ...

Literal: _SpecialForm

def IntVar(name: str) -> Any: ...  # returns a new TypeVar

# Internal mypy fallback type for all typed dicts (does not exist at runtime)
# N.B. Keep this mostly in sync with typing._TypedDict/mypy_extensions._TypedDict
@type_check_only
class _TypedDict(Mapping[str, object], metaclass=abc.ABCMeta):
    __total__: ClassVar[bool]
    __orig_bases__: ClassVar[tuple[Any, ...]]
    def copy(self) -> Self: ...
    # Using Never so that only calls using mypy plugin hook that specialize the signature
    # can go through.
    def setdefault(self, k: Never, default: object) -> object: ...
    # Mypy plugin hook for 'pop' expects that 'default' has a type variable type.
    def pop(self, k: Never, default: _T = ...) -> object: ...  # pyright: ignore[reportInvalidTypeVarUse]
    def update(self: _T, __m: _T) -> None: ...
    def items(self) -> ItemsView[str, object]: ...
    def keys(self) -> KeysView[str]: ...
    def values(self) -> ValuesView[object]: ...
    def __delitem__(self, k: Never) -> None: ...

# TypedDict is a (non-subscriptable) special form.
TypedDict: object

OrderedDict = _Alias()

def get_type_hints(
    obj: Callable[..., Any],
    globalns: dict[str, Any] | None = None,
    localns: dict[str, Any] | None = None,
    include_extras: bool = False,
) -> dict[str, Any]: ...
def get_args(tp: Any) -> tuple[Any, ...]: ...
@overload
def get_origin(tp: UnionType) -> type[UnionType]: ...
@overload
def get_origin(tp: GenericAlias) -> type: ...
@overload
def get_origin(tp: Any) -> Any | None: ...

Annotated: _SpecialForm
_AnnotatedAlias: Any  # undocumented

@runtime_checkable
class SupportsIndex(Protocol, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __index__(self) -> int: ...

class TypeVar:
    @property
    def __name__(self) -> str: ...
    @property
    def __bound__(self) -> Any | None: ...
    @property
    def __constraints__(self) -> tuple[Any, ...]: ...
    @property
    def __covariant__(self) -> bool: ...
    @property
    def __contravariant__(self) -> bool: ...
    @property
    def __infer_variance__(self) -> bool: ...
    @property
    def __default__(self) -> Any | None: ...
    def __init__(
        self,
        name: str,
        *constraints: Any,
        bound: Any | None = None,
        covariant: bool = False,
        contravariant: bool = False,
        default: Any | None = None,
        infer_variance: bool = False,
    ) -> None: ...

class ParamSpec: ...
class TypeVarTuple: ...
