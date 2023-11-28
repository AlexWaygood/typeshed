import abc
import sys
import typing
from _typeshed import Incomplete
from typing import (  # noqa: Y022,Y037,Y038,Y039
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
    Mapping as Mapping,
    MappingView as MappingView,
    MutableMapping as MutableMapping,
    MutableSequence as MutableSequence,
    MutableSet as MutableSet,
    NoReturn as NoReturn,
    Optional as Optional,
    Reversible as Reversible,
    Sequence as Sequence,
    Set as Set,
    Sized as Sized,
    SupportsAbs as SupportsAbs,
    SupportsBytes as SupportsBytes,
    SupportsFloat as SupportsFloat,
    SupportsInt as SupportsInt,
    SupportsRound as SupportsRound,
    Text as Text,
    TextIO as TextIO,
    Tuple as Tuple,
    Type as Type,
    Union as Union,
    ValuesView as ValuesView,
    _Alias,
    cast as cast,
    no_type_check as no_type_check,
    no_type_check_decorator as no_type_check_decorator,
    overload as overload,
    type_check_only,
)

if sys.version_info >= (3, 10):
    from types import UnionType
if sys.version_info >= (3, 9):
    from types import GenericAlias

_T = typing.TypeVar("_T")
_F = typing.TypeVar("_F", bound=Callable[..., Any])
_TC = typing.TypeVar("_TC", bound=type[object])

# unfortunately we have to duplicate this class definition from typing.pyi or we break pytype
class _SpecialForm:
    def __getitem__(self, parameters: Any) -> object: ...
    if sys.version_info >= (3, 10):
        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...

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
    if sys.version_info >= (3, 9):
        @overload
        def __or__(self, __value: Self) -> Self: ...
        @overload
        def __or__(self, __value: dict[str, Any]) -> dict[str, object]: ...
        @overload
        def __ror__(self, __value: Self) -> Self: ...
        @overload
        def __ror__(self, __value: dict[str, Any]) -> dict[str, object]: ...
        # supposedly incompatible definitions of `__ior__` and `__or__`:
        def __ior__(self, __value: Self) -> Self: ...  # type: ignore[misc]

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

if sys.version_info >= (3, 10):
    @overload
    def get_origin(tp: UnionType) -> type[UnionType]: ...

if sys.version_info >= (3, 9):
    @overload
    def get_origin(tp: GenericAlias) -> type: ...

@overload
def get_origin(tp: ParamSpecArgs | ParamSpecKwargs) -> ParamSpec: ...
@overload
def get_origin(tp: Any) -> Any | None: ...

Annotated: _SpecialForm
_AnnotatedAlias: Any  # undocumented

@runtime_checkable
class SupportsIndex(Protocol, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __index__(self) -> int: ...

# New and changed things in 3.10
if sys.version_info >= (3, 10):
    from typing import (
        Concatenate as Concatenate,
        NewType as NewType,
        ParamSpecArgs as ParamSpecArgs,
        ParamSpecKwargs as ParamSpecKwargs,
        TypeAlias as TypeAlias,
        TypeGuard as TypeGuard,
    )

from typing import (
    LiteralString as LiteralString,
    NamedTuple as NamedTuple,
    Never as Never,
    NotRequired as NotRequired,
    Required as Required,
    Self as Self,
    Unpack as Unpack,
)

# New things in 3.xx
# The `default` parameter was added to TypeVar, ParamSpec, and TypeVarTuple (PEP 696)
# The `infer_variance` parameter was added to TypeVar in 3.12 (PEP 695)
# typing_extensions.override (PEP 698)
@final
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
    if sys.version_info >= (3, 10):
        def __or__(self, right: Any) -> _SpecialForm: ...
        def __ror__(self, left: Any) -> _SpecialForm: ...
    if sys.version_info >= (3, 11):
        def __typing_subst__(self, arg: Incomplete) -> Incomplete: ...

@final
class ParamSpec:
    @property
    def __name__(self) -> str: ...
    @property
    def __bound__(self) -> Any | None: ...
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
        *,
        bound: None | type[Any] | str = None,
        contravariant: bool = False,
        covariant: bool = False,
        default: type[Any] | str | None = None,
    ) -> None: ...
    @property
    def args(self) -> ParamSpecArgs: ...
    @property
    def kwargs(self) -> ParamSpecKwargs: ...

@final
class TypeVarTuple:
    @property
    def __name__(self) -> str: ...
    @property
    def __default__(self) -> Any | None: ...
    def __init__(self, name: str, *, default: Any | None = None) -> None: ...
    def __iter__(self) -> Any: ...  # Unpack[Self]

from collections.abc import Buffer as Buffer
from types import get_original_bases as get_original_bases

class Doc:
    documentation: str
    def __init__(self, __documentation: str) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
