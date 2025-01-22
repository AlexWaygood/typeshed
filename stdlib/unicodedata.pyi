import sys
from _typeshed import ReadOnlyBuffer
from typing import Any, Literal, TypeVar, final, overload
from typing_extensions import TypeAlias

ucd_3_2_0: UCD
unidata_version: str

if sys.version_info < (3, 10):
    ucnhash_CAPI: Any

_T = TypeVar("_T")

_NormalizationForm: TypeAlias = Literal["NFC", "NFD", "NFKC", "NFKD"]

def bidirectional(chr: str, /) -> str: ...
def category(chr: str, /) -> str: ...
def combining(chr: str, /) -> int: ...
@overload
def decimal(chr: str, /) -> int: ...
@overload
def decimal[_T](chr: str, default: _T, /) -> int | _T: ...
def decomposition(chr: str, /) -> str: ...
@overload
def digit(chr: str, /) -> int: ...
@overload
def digit[_T](chr: str, default: _T, /) -> int | _T: ...

_EastAsianWidth: TypeAlias = Literal["F", "H", "W", "Na", "A", "N"]

def east_asian_width(chr: str, /) -> _EastAsianWidth: ...
def is_normalized(form: _NormalizationForm, unistr: str, /) -> bool: ...
def lookup(name: str | ReadOnlyBuffer, /) -> str: ...
def mirrored(chr: str, /) -> int: ...
@overload
def name(chr: str, /) -> str: ...
@overload
def name[_T](chr: str, default: _T, /) -> str | _T: ...
def normalize(form: _NormalizationForm, unistr: str, /) -> str: ...
@overload
def numeric(chr: str, /) -> float: ...
@overload
def numeric[_T](chr: str, default: _T, /) -> float | _T: ...
@final
class UCD:
    # The methods below are constructed from the same array in C
    # (unicodedata_functions) and hence identical to the functions above.
    unidata_version: str
    def bidirectional(self, chr: str, /) -> str: ...
    def category(self, chr: str, /) -> str: ...
    def combining(self, chr: str, /) -> int: ...
    @overload
    def decimal(self, chr: str, /) -> int: ...
    @overload
    def decimal(self, chr: str, default: _T, /) -> int | _T: ...
    def decomposition(self, chr: str, /) -> str: ...
    @overload
    def digit(self, chr: str, /) -> int: ...
    @overload
    def digit(self, chr: str, default: _T, /) -> int | _T: ...
    def east_asian_width(self, chr: str, /) -> _EastAsianWidth: ...
    def is_normalized(self, form: _NormalizationForm, unistr: str, /) -> bool: ...
    def lookup(self, name: str | ReadOnlyBuffer, /) -> str: ...
    def mirrored(self, chr: str, /) -> int: ...
    @overload
    def name(self, chr: str, /) -> str: ...
    @overload
    def name(self, chr: str, default: _T, /) -> str | _T: ...
    def normalize(self, form: _NormalizationForm, unistr: str, /) -> str: ...
    @overload
    def numeric(self, chr: str, /) -> float: ...
    @overload
    def numeric(self, chr: str, default: _T, /) -> float | _T: ...
