import collections.abc  # noqa: F401
from typing import Any, MutableMapping, MutableSequence, Sequence, TypeVar  # noqa: Y022
from typing_extensions import Literal, TypeAlias

SupportsRichComparison = Any
SupportsRichComparisonT = Any

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

class object: ...
class staticmethod: ...
class classmethod: ...
class type: ...
class function: ...
class property: ...
class ellipsis: ...
class BaseException: ...
class int: ...
class float: ...
class bytes(Sequence[int]): ...
class bool(int): ...
class slice: ...
class str(Sequence[str]): ...
class list(MutableSequence[_T]): ...
class tuple(Sequence[_T_co]): ...
class dict(MutableMapping[_KT, _VT]): ...

_PositiveInteger: TypeAlias = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
_NegativeInteger: TypeAlias = Literal[-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20]
_LiteralInteger = _PositiveInteger | _NegativeInteger | Literal[0]  # noqa: Y026

Ellipsis: ellipsis
