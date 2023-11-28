import collections  # noqa
from _typeshed import Incomplete, SupportsKeysAndGetItem
from abc import ABCMeta, abstractmethod

# This itself is only available during type checking
def type_check_only(func_or_cls: _F) -> _F: ...

Any = object()

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
    def __init__(
        self,
        name: str,
        *constraints: Any,
        bound: Any | None = None,
        covariant: bool = False,
        contravariant: bool = False,
        infer_variance: bool = False,
    ) -> None: ...

# Used for an undocumented mypy feature. Does not exist at runtime.
_promote = object()

# N.B. Keep this definition in sync with typing_extensions._SpecialForm
class _SpecialForm:
    def __getitem__(self, parameters: Any) -> object: ...

_F = TypeVar("_F", bound=Callable[..., Any])
_T = TypeVar("_T")

def overload(func: _F) -> _F: ...

Union: _SpecialForm
Generic: _SpecialForm
# Protocol is only present in 3.8 and later, but mypy needs it unconditionally
Protocol: _SpecialForm
Callable: _SpecialForm
Type: _SpecialForm
NoReturn: _SpecialForm
ClassVar: _SpecialForm

Optional: _SpecialForm
Tuple: _SpecialForm
Final: _SpecialForm

def final(f: _T) -> _T: ...

Literal: _SpecialForm
# TypedDict is a (non-subscriptable) special form.
TypedDict: object

Self: _SpecialForm
Never: _SpecialForm
Unpack: _SpecialForm
Required: _SpecialForm
NotRequired: _SpecialForm
LiteralString: _SpecialForm

class TypeVarTuple:
    @property
    def __name__(self) -> str: ...
    def __init__(self, name: str) -> None: ...
    def __iter__(self) -> Any: ...
    def __typing_subst__(self, arg: Never) -> Never: ...
    def __typing_prepare_subst__(self, alias: Incomplete, args: Incomplete) -> Incomplete: ...

class ParamSpecArgs:
    @property
    def __origin__(self) -> ParamSpec: ...
    def __init__(self, origin: ParamSpec) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class ParamSpecKwargs:
    @property
    def __origin__(self) -> ParamSpec: ...
    def __init__(self, origin: ParamSpec) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class ParamSpec:
    @property
    def __name__(self) -> str: ...
    @property
    def __bound__(self) -> Any | None: ...
    @property
    def __covariant__(self) -> bool: ...
    @property
    def __contravariant__(self) -> bool: ...
    def __init__(
        self,
        name: str,
        *,
        bound: Any | None = None,
        contravariant: bool = False,
        covariant: bool = False,
        infer_variance: bool = False,
    ) -> None: ...
    @property
    def args(self) -> ParamSpecArgs: ...
    @property
    def kwargs(self) -> ParamSpecKwargs: ...
    def __or__(self, right: Any) -> _SpecialForm: ...
    def __ror__(self, left: Any) -> _SpecialForm: ...

Concatenate: _SpecialForm
TypeAlias: _SpecialForm
TypeGuard: _SpecialForm

class NewType:
    def __init__(self, name: str, tp: Any) -> None: ...
    def __call__(self, __x: _T) -> _T: ...
    def __or__(self, other: Any) -> _SpecialForm: ...
    def __ror__(self, other: Any) -> _SpecialForm: ...
    __supertype__: type

# These type variables are used by the container types.
_S = TypeVar("_S")
_KT = TypeVar("_KT")  # Key type.
_VT = TypeVar("_VT")  # Value type.
_T_co = TypeVar("_T_co", covariant=True)  # Any type covariant containers.
_KT_co = TypeVar("_KT_co", covariant=True)  # Key type covariant containers.
_VT_co = TypeVar("_VT_co", covariant=True)  # Value type covariant containers.
_TC = TypeVar("_TC", bound=Type[object])

def no_type_check(arg: _F) -> _F: ...

# Type aliases and type constructors

class _Alias:
    # Class for defining generic aliases for library types.
    def __getitem__(self, typeargs: Any) -> Any: ...

# Predefined type variables.
AnyStr = TypeVar("AnyStr", str, bytes)  # noqa: Y001

# Technically in 3.7 this inherited from GenericMeta. But let's not reflect that, since
# type checkers tend to assume that Protocols all have the ABCMeta metaclass.
class _ProtocolMeta(ABCMeta):
    def __init__(cls, *args: Any, **kwargs: Any) -> None: ...

# Abstract base classes.

def runtime_checkable(cls: _TC) -> _TC: ...
@runtime_checkable
class SupportsInt(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __int__(self) -> int: ...

@runtime_checkable
class SupportsFloat(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __float__(self) -> float: ...

@runtime_checkable
class SupportsBytes(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __bytes__(self) -> bytes: ...

@runtime_checkable
class SupportsIndex(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __index__(self) -> int: ...

@runtime_checkable
class SupportsAbs(Protocol[_T_co]):
    @abstractmethod
    def __abs__(self) -> _T_co: ...

@runtime_checkable
class SupportsRound(Protocol[_T_co]):
    @overload
    @abstractmethod
    def __round__(self) -> int: ...
    @overload
    @abstractmethod
    def __round__(self, __ndigits: int) -> _T_co: ...

@runtime_checkable
class Sized(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __len__(self) -> int: ...

@runtime_checkable
class Hashable(Protocol, metaclass=ABCMeta):
    # TODO: This is special, in that a subclass of a hashable class may not be hashable
    #   (for example, list vs. object). It's not obvious how to represent this. This class
    #   is currently mostly useless for static checking.
    @abstractmethod
    def __hash__(self) -> int: ...

@runtime_checkable
class Iterable(Protocol[_T_co]):
    @abstractmethod
    def __iter__(self) -> Iterator[_T_co]: ...

@runtime_checkable
class Iterator(Iterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __next__(self) -> _T_co: ...
    def __iter__(self) -> Iterator[_T_co]: ...

@runtime_checkable
class Reversible(Iterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __reversed__(self) -> Iterator[_T_co]: ...

_YieldT_co = TypeVar("_YieldT_co", covariant=True)
_SendT_contra = TypeVar("_SendT_contra", contravariant=True)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)

class Generator(Iterator[_YieldT_co], Generic[_YieldT_co, _SendT_contra, _ReturnT_co]):
    def __next__(self) -> _YieldT_co: ...
    @abstractmethod
    def send(self, __value: _SendT_contra) -> _YieldT_co: ...
    def close(self) -> None: ...
    def __iter__(self) -> Generator[_YieldT_co, _SendT_contra, _ReturnT_co]: ...

@runtime_checkable
class Awaitable(Protocol[_T_co]):
    @abstractmethod
    def __await__(self) -> Generator[Any, None, _T_co]: ...

class Coroutine(Awaitable[_ReturnT_co], Generic[_YieldT_co, _SendT_contra, _ReturnT_co]):
    def __await__(self) -> Generator[Any, None, _T_co]: ...

# NOTE: This type does not exist in typing.py or PEP 484 but mypy needs it to exist.
# The parameters correspond to Generator, but the 4th is the original type.
@type_check_only
class AwaitableGenerator(
    Awaitable[_ReturnT_co],
    Generator[_YieldT_co, _SendT_contra, _ReturnT_co],
    Generic[_YieldT_co, _SendT_contra, _ReturnT_co, _S],
    metaclass=ABCMeta,
): ...

@runtime_checkable
class AsyncIterable(Protocol[_T_co]):
    @abstractmethod
    def __aiter__(self) -> AsyncIterator[_T_co]: ...

@runtime_checkable
class AsyncIterator(AsyncIterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __anext__(self) -> Awaitable[_T_co]: ...
    def __aiter__(self) -> AsyncIterator[_T_co]: ...

class AsyncGenerator(AsyncIterator[_YieldT_co], Generic[_YieldT_co, _SendT_contra]):
    def __anext__(self) -> Awaitable[_YieldT_co]: ...

@runtime_checkable
class Container(Protocol[_T_co]):
    # This is generic more on vibes than anything else
    @abstractmethod
    def __contains__(self, __x: object) -> bool: ...

@runtime_checkable
class Collection(Iterable[_T_co], Container[_T_co], Protocol[_T_co]):
    # Implement Sized (but don't have it as a base class).
    @abstractmethod
    def __len__(self) -> int: ...

class Sequence(Collection[_T_co], Reversible[_T_co]):
    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> _T_co: ...
    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence[_T_co]: ...
    # Mixin methods
    def index(self, value: Any, start: int = 0, stop: int = ...) -> int: ...
    def count(self, value: Any) -> int: ...
    def __contains__(self, value: object) -> bool: ...
    def __iter__(self) -> Iterator[_T_co]: ...
    def __reversed__(self) -> Iterator[_T_co]: ...

class MutableSequence(Sequence[_T]):
    @abstractmethod
    def insert(self, index: int, value: _T) -> None: ...
    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> _T: ...
    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> MutableSequence[_T]: ...
    @overload
    @abstractmethod
    def __setitem__(self, index: int, value: _T) -> None: ...
    @overload
    @abstractmethod
    def __setitem__(self, index: slice, value: Iterable[_T]) -> None: ...
    @overload
    @abstractmethod
    def __delitem__(self, index: int) -> None: ...
    @overload
    @abstractmethod
    def __delitem__(self, index: slice) -> None: ...
    # Mixin methods
    def append(self, value: _T) -> None: ...
    def clear(self) -> None: ...
    def extend(self, values: Iterable[_T]) -> None: ...
    def reverse(self) -> None: ...
    def pop(self, index: int = -1) -> _T: ...
    def remove(self, value: _T) -> None: ...

class AbstractSet(Collection[_T_co]):
    @abstractmethod
    def __contains__(self, x: object) -> bool: ...
    def _hash(self) -> int: ...
    # Mixin methods
    def __le__(self, other: AbstractSet[Any]) -> bool: ...
    def __lt__(self, other: AbstractSet[Any]) -> bool: ...
    def __gt__(self, other: AbstractSet[Any]) -> bool: ...
    def __ge__(self, other: AbstractSet[Any]) -> bool: ...
    def __and__(self, other: AbstractSet[Any]) -> AbstractSet[_T_co]: ...
    def __or__(self, other: AbstractSet[_T]) -> AbstractSet[_T_co | _T]: ...
    def __sub__(self, other: AbstractSet[Any]) -> AbstractSet[_T_co]: ...
    def __xor__(self, other: AbstractSet[_T]) -> AbstractSet[_T_co | _T]: ...
    def __eq__(self, other: object) -> bool: ...
    def isdisjoint(self, other: Iterable[Any]) -> bool: ...

class MutableSet(AbstractSet[_T]):
    @abstractmethod
    def add(self, value: _T) -> None: ...
    @abstractmethod
    def discard(self, value: _T) -> None: ...
    # Mixin methods
    def clear(self) -> None: ...
    def pop(self) -> _T: ...
    def remove(self, value: _T) -> None: ...

class MappingView(Sized):
    def __init__(self, mapping: Mapping[Any, Any]) -> None: ...  # undocumented
    def __len__(self) -> int: ...

class ItemsView(MappingView, AbstractSet[tuple[_KT_co, _VT_co]], Generic[_KT_co, _VT_co]):
    def __init__(self, mapping: Mapping[_KT_co, _VT_co]) -> None: ...  # undocumented
    def __and__(self, other: Iterable[Any]) -> set[tuple[_KT_co, _VT_co]]: ...
    def __rand__(self, other: Iterable[_T]) -> set[_T]: ...
    def __contains__(self, item: object) -> bool: ...
    def __iter__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...
    def __or__(self, other: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __ror__(self, other: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __sub__(self, other: Iterable[Any]) -> set[tuple[_KT_co, _VT_co]]: ...
    def __rsub__(self, other: Iterable[_T]) -> set[_T]: ...
    def __xor__(self, other: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __rxor__(self, other: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...

class KeysView(MappingView, AbstractSet[_KT_co]):
    def __init__(self, mapping: Mapping[_KT_co, Any]) -> None: ...  # undocumented
    def __and__(self, other: Iterable[Any]) -> set[_KT_co]: ...
    def __rand__(self, other: Iterable[_T]) -> set[_T]: ...
    def __contains__(self, key: object) -> bool: ...
    def __iter__(self) -> Iterator[_KT_co]: ...
    def __or__(self, other: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __ror__(self, other: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __sub__(self, other: Iterable[Any]) -> set[_KT_co]: ...
    def __rsub__(self, other: Iterable[_T]) -> set[_T]: ...
    def __xor__(self, other: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __rxor__(self, other: Iterable[_T]) -> set[_KT_co | _T]: ...

class ValuesView(MappingView, Collection[_VT_co]):
    def __init__(self, mapping: Mapping[Any, _VT_co]) -> None: ...  # undocumented
    def __contains__(self, value: object) -> bool: ...
    def __iter__(self) -> Iterator[_VT_co]: ...

class Mapping(Collection[_KT], Generic[_KT, _VT_co]):
    # TODO: We wish the key type could also be covariant, but that doesn't work,
    # see discussion in https://github.com/python/typing/pull/273.
    @abstractmethod
    def __getitem__(self, __key: _KT) -> _VT_co: ...
    # Mixin methods
    @overload
    def get(self, __key: _KT) -> _VT_co | None: ...
    @overload
    def get(self, __key: _KT, default: _VT_co | _T) -> _VT_co | _T: ...
    def items(self) -> ItemsView[_KT, _VT_co]: ...
    def keys(self) -> KeysView[_KT]: ...
    def values(self) -> ValuesView[_VT_co]: ...
    def __contains__(self, __key: object) -> bool: ...
    def __eq__(self, __other: object) -> bool: ...

class MutableMapping(Mapping[_KT, _VT]):
    @abstractmethod
    def __setitem__(self, __key: _KT, __value: _VT) -> None: ...
    @abstractmethod
    def __delitem__(self, __key: _KT) -> None: ...
    def clear(self) -> None: ...
    @overload
    def pop(self, __key: _KT) -> _VT: ...
    @overload
    def pop(self, __key: _KT, default: _VT) -> _VT: ...
    @overload
    def pop(self, __key: _KT, default: _T) -> _VT | _T: ...
    def popitem(self) -> tuple[_KT, _VT]: ...
    # This overload should be allowed only if the value type is compatible with None.
    #
    # Keep the following methods in line with MutableMapping.setdefault, modulo positional-only differences:
    # -- collections.OrderedDict.setdefault
    # -- collections.ChainMap.setdefault
    # -- weakref.WeakKeyDictionary.setdefault
    @overload
    def setdefault(self: MutableMapping[_KT, _T | None], __key: _KT, __default: None = None) -> _T | None: ...
    @overload
    def setdefault(self, __key: _KT, __default: _VT) -> _VT: ...
    # 'update' used to take a Union, but using overloading is better.
    # The second overloaded type here is a bit too general, because
    # Mapping[tuple[_KT, _VT], W] is a subclass of Iterable[tuple[_KT, _VT]],
    # but will always have the behavior of the first overloaded type
    # at runtime, leading to keys of a mix of types _KT and tuple[_KT, _VT].
    # We don't currently have any way of forcing all Mappings to use
    # the first overload, but by using overloading rather than a Union,
    # mypy will commit to using the first overload when the argument is
    # known to be a Mapping with unknown type parameters, which is closer
    # to the behavior we want. See mypy issue  #1430.
    #
    # Various mapping classes have __ior__ methods that should be kept roughly in line with .update():
    # -- dict.__ior__
    # -- os._Environ.__ior__
    # -- collections.UserDict.__ior__
    # -- collections.ChainMap.__ior__
    # -- peewee.attrdict.__add__
    # -- peewee.attrdict.__iadd__
    # -- weakref.WeakValueDictionary.__ior__
    # -- weakref.WeakKeyDictionary.__ior__
    @overload
    def update(self, __m: SupportsKeysAndGetItem[_KT, _VT], **kwargs: _VT) -> None: ...
    @overload
    def update(self, __m: Iterable[tuple[_KT, _VT]], **kwargs: _VT) -> None: ...
    @overload
    def update(self, **kwargs: _VT) -> None: ...

Text = str

TYPE_CHECKING: bool

# In stubs, the arguments of the IO class are marked as positional-only.
# This differs from runtime, but better reflects the fact that in reality
# classes deriving from IO use different names for the arguments.
class IO(Iterator[AnyStr]):
    # At runtime these are all abstract properties,
    # but making them abstract in the stub is hugely disruptive, for not much gain.
    # See #8726
    @property
    def mode(self) -> str: ...
    # Usually str, but may be bytes if a bytes path was passed to open(). See #10737.
    # If PEP 696 becomes available, we may want to use a defaulted TypeVar here.
    @property
    def name(self) -> str | Any: ...
    @abstractmethod
    def close(self) -> None: ...
    @property
    def closed(self) -> bool: ...
    @abstractmethod
    def fileno(self) -> int: ...
    @abstractmethod
    def flush(self) -> None: ...
    @abstractmethod
    def isatty(self) -> bool: ...
    @abstractmethod
    def read(self, __n: int = -1) -> AnyStr: ...
    @abstractmethod
    def readable(self) -> bool: ...
    @abstractmethod
    def readline(self, __limit: int = -1) -> AnyStr: ...
    @abstractmethod
    def readlines(self, __hint: int = -1) -> list[AnyStr]: ...
    @abstractmethod
    def seek(self, __offset: int, __whence: int = 0) -> int: ...
    @abstractmethod
    def seekable(self) -> bool: ...
    @abstractmethod
    def tell(self) -> int: ...
    @abstractmethod
    def truncate(self, __size: int | None = None) -> int: ...
    @abstractmethod
    def writable(self) -> bool: ...
    @abstractmethod
    def __next__(self) -> AnyStr: ...
    @abstractmethod
    def __iter__(self) -> Iterator[AnyStr]: ...

class BinaryIO: ...

class TextIO:
    # See comment regarding the @properties in the `IO` class
    @property
    def buffer(self) -> BinaryIO: ...
    @property
    def encoding(self) -> str: ...
    @property
    def errors(self) -> str | None: ...
    @property
    def line_buffering(self) -> int: ...  # int on PyPy, bool on CPython
    @property
    def newlines(self) -> Any: ...  # None, str or tuple

ByteString = bytes

@overload
def cast(typ: Type[_T], val: Any) -> _T: ...
@overload
def cast(typ: str, val: Any) -> Any: ...
@overload
def cast(typ: object, val: Any) -> Any: ...

# Type constructors

class NamedTuple(tuple[Any, ...]):
    _field_defaults: ClassVar[dict[str, Any]]
    _fields: ClassVar[tuple[str, ...]]
    @overload
    def __init__(self, __typename: str, __fields: Iterable[tuple[str, Any]]) -> None: ...
    @overload
    def __init__(self, __typename: str, __fields: None = None, **kwargs: Any) -> None: ...
    @classmethod
    def _make(cls, iterable: Iterable[Any]) -> NamedTuple: ...
    def _asdict(self) -> dict[str, Any]: ...
    def _replace(self, **kwargs: Any) -> NamedTuple: ...

class _TypedDict(Mapping[str, object], metaclass=ABCMeta):
    __total__: ClassVar[bool]
    # __orig_bases__ sometimes exists on <3.12, but not consistently,
    # so we only add it to the stub on 3.12+
    # Using Never so that only calls using mypy plugin hook that specialize the signature
    # can go through.
    def setdefault(self, k: NoReturn, default: object) -> object: ...
    # Mypy plugin hook for 'pop' expects that 'default' has a type variable type.
    def pop(self, k: NoReturn, default: _T = ...) -> object: ...  # pyright: ignore[reportInvalidTypeVarUse]
    def update(self: _T, __m: _T) -> None: ...
    def __delitem__(self, k: NoReturn) -> None: ...
    def items(self) -> ItemsView[str, object]: ...
    def keys(self) -> KeysView[str]: ...
    def values(self) -> ValuesView[object]: ...

class ForwardRef:
    def __init__(self, arg: str, is_argument: bool = True, module: Any | None = None, *, is_class: bool = False) -> None: ...
    def _evaluate(
        self, globalns: dict[str, Any] | None, localns: dict[str, Any] | None, recursive_guard: AbstractSet[str]
    ) -> Any | None: ...
