import abc  # noqa: F401
import collections  # noqa: F401

Any = object()

class TypeVar: ...
class _SpecialForm: ...

_T = TypeVar("_T")

Generic: _SpecialForm
Protocol: _SpecialForm
Callable: _SpecialForm
Literal: _SpecialForm
TypeAlias: _SpecialForm

_KT = TypeVar("_KT")  # Key type.
_VT = TypeVar("_VT")  # Value type.
_T_co = TypeVar("_T_co", covariant=True)  # Any type covariant containers.
_KT_co = TypeVar("_KT_co", covariant=True)  # Key type covariant containers.
_VT_co = TypeVar("_VT_co", covariant=True)  # Value type covariant containers.

class _Alias:
    def __getitem__(self, typeargs: Any) -> Any: ...

class Sized(Protocol): ...
class Iterable(Protocol[_T_co]): ...
class Iterator(Iterable[_T_co], Protocol[_T_co]): ...
class Generator(Iterator[_T_co]): ...
class Collection(Iterable[_T_co]): ...
class Sequence(Collection[_T_co]): ...
class MutableSequence(Sequence[_T]): ...
class AbstractSet(Collection[_T_co]): ...
class MappingView(Sized): ...
class ItemsView(MappingView, AbstractSet[tuple[_KT_co, _VT_co]]): ...
class KeysView(MappingView, AbstractSet[_KT_co]): ...
class ValuesView(MappingView, Collection[_VT_co]): ...
class Mapping(Collection[_KT], Generic[_KT, _VT_co]): ...
class MutableMapping(Mapping[_KT, _VT]): ...
