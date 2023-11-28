import abc  # noqa: F401
import collections  # noqa: F401

Any = object()

class TypeVar: ...
class _SpecialForm: ...

Generic: _SpecialForm
Callable: _SpecialForm
Literal: _SpecialForm
TypeAlias: _SpecialForm
