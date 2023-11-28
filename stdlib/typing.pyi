import abc  # noqa: F401
import collections  # noqa: F401

class TypeVar: ...
class _SpecialForm: ...

Generic: _SpecialForm
Callable: _SpecialForm
TypeAlias: _SpecialForm
