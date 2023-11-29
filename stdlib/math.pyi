import sys
from collections.abc import Iterable
from typing import Protocol, SupportsFloat, TypeVar, overload
from typing_extensions import SupportsIndex, TypeAlias

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)

if sys.version_info >= (3, 8):
    _SupportsFloatOrIndex: TypeAlias = SupportsFloat | SupportsIndex
else:
    _SupportsFloatOrIndex: TypeAlias = SupportsFloat

e: float
pi: float
inf: float
nan: float
tau: float

def acos(__x: _SupportsFloatOrIndex) -> float: ...
def acosh(__x: _SupportsFloatOrIndex) -> float: ...
def asin(__x: _SupportsFloatOrIndex) -> float: ...
def asinh(__x: _SupportsFloatOrIndex) -> float: ...
def atan(__x: _SupportsFloatOrIndex) -> float: ...
def atan2(__y: _SupportsFloatOrIndex, __x: _SupportsFloatOrIndex) -> float: ...
def atanh(__x: _SupportsFloatOrIndex) -> float: ...

if sys.version_info >= (3, 11):
    def cbrt(__x: _SupportsFloatOrIndex) -> float: ...

class _SupportsCeil(Protocol[_T_co]):
    def __ceil__(self) -> _T_co: ...

@overload
def ceil(__x: _SupportsCeil[_T]) -> _T: ...
@overload
def ceil(__x: _SupportsFloatOrIndex) -> int: ...

if sys.version_info >= (3, 8):
    def comb(__n: SupportsIndex, __k: SupportsIndex) -> int: ...

def copysign(__x: _SupportsFloatOrIndex, __y: _SupportsFloatOrIndex) -> float: ...
def cos(__x: _SupportsFloatOrIndex) -> float: ...
def cosh(__x: _SupportsFloatOrIndex) -> float: ...
def degrees(__x: _SupportsFloatOrIndex) -> float: ...

if sys.version_info >= (3, 8):
    def dist(__p: Iterable[_SupportsFloatOrIndex], __q: Iterable[_SupportsFloatOrIndex]) -> float: ...

def erf(__x: _SupportsFloatOrIndex) -> float: ...
def erfc(__x: _SupportsFloatOrIndex) -> float: ...
def exp(__x: _SupportsFloatOrIndex) -> float: ...

if sys.version_info >= (3, 11):
    def exp2(__x: _SupportsFloatOrIndex) -> float: ...

def expm1(__x: _SupportsFloatOrIndex) -> float: ...
def fabs(__x: _SupportsFloatOrIndex) -> float: ...

if sys.version_info >= (3, 8):
    def factorial(__x: SupportsIndex) -> int: ...

else:
    def factorial(__x: int) -> int: ...

class _SupportsFloor(Protocol[_T_co]):
    def __floor__(self) -> _T_co: ...

@overload
def floor(__x: _SupportsFloor[_T]) -> _T: ...
@overload
def floor(__x: _SupportsFloatOrIndex) -> int: ...
def fmod(__x: _SupportsFloatOrIndex, __y: _SupportsFloatOrIndex) -> float: ...
def frexp(__x: _SupportsFloatOrIndex) -> tuple[float, int]: ...
def fsum(__seq: Iterable[_SupportsFloatOrIndex]) -> float: ...
def gamma(__x: _SupportsFloatOrIndex) -> float: ...

if sys.version_info >= (3, 9):
    def gcd(*integers: SupportsIndex) -> int: ...

else:
    def gcd(__x: SupportsIndex, __y: SupportsIndex) -> int: ...

if sys.version_info >= (3, 8):
    def hypot(*coordinates: _SupportsFloatOrIndex) -> float: ...

else:
    def hypot(__x: _SupportsFloatOrIndex, __y: _SupportsFloatOrIndex) -> float: ...

def isclose(
    a: _SupportsFloatOrIndex,
    b: _SupportsFloatOrIndex,
    *,
    rel_tol: _SupportsFloatOrIndex = 1e-09,
    abs_tol: _SupportsFloatOrIndex = 0.0,
) -> bool: ...
def isinf(__x: _SupportsFloatOrIndex) -> bool: ...
def isfinite(__x: _SupportsFloatOrIndex) -> bool: ...
def isnan(__x: _SupportsFloatOrIndex) -> bool: ...

if sys.version_info >= (3, 8):
    def isqrt(__n: SupportsIndex) -> int: ...

if sys.version_info >= (3, 9):
    def lcm(*integers: SupportsIndex) -> int: ...

def ldexp(__x: _SupportsFloatOrIndex, __i: int) -> float: ...
def lgamma(__x: _SupportsFloatOrIndex) -> float: ...
def log(x: _SupportsFloatOrIndex, base: _SupportsFloatOrIndex = ...) -> float: ...
def log10(__x: _SupportsFloatOrIndex) -> float: ...
def log1p(__x: _SupportsFloatOrIndex) -> float: ...
def log2(__x: _SupportsFloatOrIndex) -> float: ...
def modf(__x: _SupportsFloatOrIndex) -> tuple[float, float]: ...

if sys.version_info >= (3, 12):
    def nextafter(__x: _SupportsFloatOrIndex, __y: _SupportsFloatOrIndex, *, steps: SupportsIndex | None = None) -> float: ...

elif sys.version_info >= (3, 9):
    def nextafter(__x: _SupportsFloatOrIndex, __y: _SupportsFloatOrIndex) -> float: ...

if sys.version_info >= (3, 8):
    def perm(__n: SupportsIndex, __k: SupportsIndex | None = None) -> int: ...

def pow(__x: _SupportsFloatOrIndex, __y: _SupportsFloatOrIndex) -> float: ...

if sys.version_info >= (3, 8):
    @overload
    def prod(__iterable: Iterable[SupportsIndex], *, start: SupportsIndex = 1) -> int: ...  # type: ignore[overload-overlap]
    @overload
    def prod(__iterable: Iterable[_SupportsFloatOrIndex], *, start: _SupportsFloatOrIndex = 1) -> float: ...

def radians(__x: _SupportsFloatOrIndex) -> float: ...
def remainder(__x: _SupportsFloatOrIndex, __y: _SupportsFloatOrIndex) -> float: ...
def sin(__x: _SupportsFloatOrIndex) -> float: ...
def sinh(__x: _SupportsFloatOrIndex) -> float: ...

if sys.version_info >= (3, 12):
    def sumprod(__p: Iterable[float], __q: Iterable[float]) -> float: ...

def sqrt(__x: _SupportsFloatOrIndex) -> float: ...
def tan(__x: _SupportsFloatOrIndex) -> float: ...
def tanh(__x: _SupportsFloatOrIndex) -> float: ...

# Is different from `_typeshed.SupportsTrunc`, which is not generic
class _SupportsTrunc(Protocol[_T_co]):
    def __trunc__(self) -> _T_co: ...

def trunc(__x: _SupportsTrunc[_T]) -> _T: ...

if sys.version_info >= (3, 9):
    def ulp(__x: _SupportsFloatOrIndex) -> float: ...
