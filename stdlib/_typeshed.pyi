from typing import Any, Iterable, Protocol, TypeVar
from typing_extensions import TypeAlias

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)

Incomplete: TypeAlias = Any

class SupportsDunderLT(Protocol[_T_contra]):
    def __lt__(self, __other: _T_contra) -> bool: ...

class SupportsDunderGT(Protocol[_T_contra]):
    def __gt__(self, __other: _T_contra) -> bool: ...

class SupportsDunderLE(Protocol[_T_contra]):
    def __le__(self, __other: _T_contra) -> bool: ...

class SupportsDunderGE(Protocol[_T_contra]):
    def __ge__(self, __other: _T_contra) -> bool: ...

SupportsRichComparison: TypeAlias = SupportsDunderLT[Any] | SupportsDunderGT[Any]
SupportsRichComparisonT = TypeVar("SupportsRichComparisonT", bound=SupportsRichComparison)  # noqa: Y001

class SupportsKeysAndGetItem(Protocol[_KT, _VT_co]):
    def keys(self) -> Iterable[_KT]: ...
    def __getitem__(self, __key: _KT) -> _VT_co: ...

class IdentityFunction(Protocol):
    def __call__(self, __x: _T) -> _T: ...

StrPath: TypeAlias = str  # stable
BytesPath: TypeAlias = bytes  # stable
StrOrBytesPath: TypeAlias = str | bytes  # stable
WriteableBuffer: TypeAlias = bytes
ReadableBuffer: TypeAlias = bytes  # stable
