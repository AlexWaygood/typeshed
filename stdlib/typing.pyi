import abc  # noqa: F401
import collections  # noqa: F401

Any = object()

class TypeVar: ...
class _SpecialForm: ...

Generic: _SpecialForm
Callable: _SpecialForm
Literal: _SpecialForm
TypeAlias: _SpecialForm

_KT = TypeVar("_KT")
_T_co = TypeVar("_T_co", covariant=True)

class Iterable(Generic[_T_co]): ...
class Iterator(Iterable[_T_co]): ...
class Sequence(Generic[_T_co]): ...
class Mapping(Generic[_KT]): ...
