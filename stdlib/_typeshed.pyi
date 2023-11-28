# Utility types for typeshed
#
# See the README.md file in this directory for more information.

from typing import Any, Iterable, Protocol, TypeVar
from typing_extensions import Buffer, Literal, TypeAlias

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)
_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)

# Use for "self" annotations:
#   def __enter__(self: Self) -> Self: ...
Self = TypeVar("Self")  # noqa: Y001

# covariant version of typing.AnyStr, useful for protocols
AnyStr_co = TypeVar("AnyStr_co", str, bytes, covariant=True)  # noqa: Y001

# For partially known annotations. Usually, fields where type annotations
# haven't been added are left unannotated, but in some situations this
# isn't possible or a type is already partially known. In cases like these,
# use Incomplete instead of Any as a marker. For example, use
# "Incomplete | None" instead of "Any | None".
Incomplete: TypeAlias = Any

# To describe a function parameter that is unused and will work with anything.
Unused: TypeAlias = object

# Used to mark arguments that default to a sentinel value. This prevents
# stubtest from complaining about the default value not matching.
#
# def foo(x: int | None = sentinel) -> None: ...
#
# In cases where the sentinel object is exported and can be used by user code,
# a construct like this is better:
#
# _SentinelType = NewType("_SentinelType", object)
# sentinel: _SentinelType
# def foo(x: int | None | _SentinelType = ...) -> None: ...
sentinel: Any

# Comparison protocols

class SupportsDunderLT(Protocol[_T_contra]):
    def __lt__(self, __other: _T_contra) -> bool: ...

class SupportsDunderGT(Protocol[_T_contra]):
    def __gt__(self, __other: _T_contra) -> bool: ...

class SupportsDunderLE(Protocol[_T_contra]):
    def __le__(self, __other: _T_contra) -> bool: ...

class SupportsDunderGE(Protocol[_T_contra]):
    def __ge__(self, __other: _T_contra) -> bool: ...

class SupportsAllComparisons(
    SupportsDunderLT[Any], SupportsDunderGT[Any], SupportsDunderLE[Any], SupportsDunderGE[Any], Protocol
): ...

SupportsRichComparison: TypeAlias = SupportsDunderLT[Any] | SupportsDunderGT[Any]
SupportsRichComparisonT = TypeVar("SupportsRichComparisonT", bound=SupportsRichComparison)  # noqa: Y001

# Dunder protocols

# stable
class SupportsKeysAndGetItem(Protocol[_KT, _VT_co]):
    def keys(self) -> Iterable[_KT]: ...
    def __getitem__(self, __key: _KT) -> _VT_co: ...

class IdentityFunction(Protocol):
    def __call__(self, __x: _T) -> _T: ...

StrPath: TypeAlias = str  # stable
BytesPath: TypeAlias = bytes  # stable
StrOrBytesPath: TypeAlias = str | bytes  # stable

OpenTextModeUpdating: TypeAlias = Literal[
    "r+",
    "+r",
    "rt+",
    "r+t",
    "+rt",
    "tr+",
    "t+r",
    "+tr",
    "w+",
    "+w",
    "wt+",
    "w+t",
    "+wt",
    "tw+",
    "t+w",
    "+tw",
    "a+",
    "+a",
    "at+",
    "a+t",
    "+at",
    "ta+",
    "t+a",
    "+ta",
    "x+",
    "+x",
    "xt+",
    "x+t",
    "+xt",
    "tx+",
    "t+x",
    "+tx",
]
OpenTextModeWriting: TypeAlias = Literal["w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx"]
OpenTextModeReading: TypeAlias = Literal["r", "rt", "tr", "U", "rU", "Ur", "rtU", "rUt", "Urt", "trU", "tUr", "Utr"]
OpenTextMode: TypeAlias = OpenTextModeUpdating | OpenTextModeWriting | OpenTextModeReading
OpenBinaryModeUpdating: TypeAlias = Literal[
    "rb+",
    "r+b",
    "+rb",
    "br+",
    "b+r",
    "+br",
    "wb+",
    "w+b",
    "+wb",
    "bw+",
    "b+w",
    "+bw",
    "ab+",
    "a+b",
    "+ab",
    "ba+",
    "b+a",
    "+ba",
    "xb+",
    "x+b",
    "+xb",
    "bx+",
    "b+x",
    "+bx",
]
OpenBinaryModeWriting: TypeAlias = Literal["wb", "bw", "ab", "ba", "xb", "bx"]
OpenBinaryModeReading: TypeAlias = Literal["rb", "br", "rbU", "rUb", "Urb", "brU", "bUr", "Ubr"]
OpenBinaryMode: TypeAlias = OpenBinaryModeUpdating | OpenBinaryModeReading | OpenBinaryModeWriting

# stable
class HasFileno(Protocol):
    def fileno(self) -> int: ...

FileDescriptor: TypeAlias = int  # stable
FileDescriptorLike: TypeAlias = int | HasFileno  # stable
FileDescriptorOrPath: TypeAlias = int | StrOrBytesPath

# stable
class SupportsRead(Protocol[_T_co]):
    def read(self, __length: int = ...) -> _T_co: ...

# stable
class SupportsReadline(Protocol[_T_co]):
    def readline(self, __length: int = ...) -> _T_co: ...

# stable
class SupportsNoArgReadline(Protocol[_T_co]):
    def readline(self) -> _T_co: ...

# stable
class SupportsWrite(Protocol[_T_contra]):
    def write(self, __s: _T_contra) -> object: ...

# stable
class SupportsFlush(Protocol):
    def flush(self) -> object: ...

# Unfortunately PEP 688 does not allow us to distinguish read-only
# from writable buffers. We use these aliases for readability for now.
# Perhaps a future extension of the buffer protocol will allow us to
# distinguish these cases in the type system.
ReadOnlyBuffer: TypeAlias = Buffer  # stable
# Anything that implements the read-write buffer interface.
WriteableBuffer: TypeAlias = Buffer
# Same as WriteableBuffer, but also includes read-only buffer types (like bytes).
ReadableBuffer: TypeAlias = Buffer  # stable
