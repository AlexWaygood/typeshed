# Note: these stubs are incomplete. The more complex type
# signatures are currently omitted.
#
# Use SupportsComplex, SupportsFloat and SupportsIndex for return types in this module
# rather than `numbers.Complex`, `numbers.Real` and `numbers.Integral`,
# to avoid an excessive number of `type: ignore`s in subclasses of these ABCs
# (since type checkers don't see `complex` as a subtype of `numbers.Complex`,
# nor `float` as a subtype of `numbers.Real`, etc.)

import sys
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from typing import Literal, SupportsFloat, SupportsIndex, overload
from typing_extensions import TypeAlias

if sys.version_info >= (3, 11):
    from typing import SupportsComplex as _SupportsComplex
else:
    # builtins.complex didn't have a __complex__ method on older Pythons
    import typing

    _SupportsComplex: TypeAlias = typing.SupportsComplex | complex

__all__ = ["Number", "Complex", "Real", "Rational", "Integral"]

class Number(metaclass=ABCMeta):
    @abstractmethod
    def __hash__(self) -> int: ...

# See comment at the top of the file
# for why some of these return types are purposefully vague
class Complex(Number):
    @abstractmethod
    def __complex__(self) -> complex: ...
    def __bool__(self) -> bool: ...
    @property
    @abstractmethod
    def real(self) -> SupportsFloat: ...
    @property
    @abstractmethod
    def imag(self) -> SupportsFloat: ...
    @abstractmethod
    def __add__(self, other: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __radd__(self, other: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __neg__(self) -> _SupportsComplex: ...
    @abstractmethod
    def __pos__(self) -> _SupportsComplex: ...
    def __sub__(self, other: complex) -> _SupportsComplex: ...
    def __rsub__(self, other: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __mul__(self, other: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __rmul__(self, other: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __truediv__(self, other: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __rtruediv__(self, other: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __pow__(self, exponent: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __rpow__(self, base: complex) -> _SupportsComplex: ...
    @abstractmethod
    def __abs__(self) -> SupportsFloat: ...
    @abstractmethod
    def conjugate(self) -> _SupportsComplex: ...
    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

# See comment at the top of the file
# for why some of these return types are purposefully vague
class Real(Complex, SupportsFloat):
    @abstractmethod
    def __float__(self) -> float: ...
    @abstractmethod
    def __trunc__(self) -> SupportsIndex: ...
    @abstractmethod
    def __floor__(self) -> SupportsIndex: ...
    @abstractmethod
    def __ceil__(self) -> SupportsIndex: ...
    @abstractmethod
    @overload
    def __round__(self, ndigits: None = None) -> SupportsIndex: ...
    @abstractmethod
    @overload
    def __round__(self, ndigits: int) -> SupportsFloat: ...
    def __divmod__(self, other: float) -> tuple[SupportsFloat, SupportsFloat]: ...
    def __rdivmod__(self, other: float) -> tuple[SupportsFloat, SupportsFloat]: ...
    @abstractmethod
    def __floordiv__(self, other: float) -> SupportsFloat: ...
    @abstractmethod
    def __rfloordiv__(self, other: float) -> SupportsFloat: ...
    @abstractmethod
    def __mod__(self, other: float) -> SupportsFloat: ...
    @abstractmethod
    def __rmod__(self, other: float) -> SupportsFloat: ...
    @abstractmethod
    def __lt__(self, other: float) -> bool: ...
    @abstractmethod
    def __le__(self, other: float) -> bool: ...
    def __complex__(self) -> complex: ...
    @property
    def real(self) -> SupportsFloat: ...
    @property
    def imag(self) -> Literal[0]: ...
    def conjugate(self) -> SupportsFloat: ...  # type: ignore[override]

# See comment at the top of the file
# for why some of these return types are purposefully vague
class Rational(Real):
    @property
    @abstractmethod
    def numerator(self) -> SupportsIndex: ...
    @property
    @abstractmethod
    def denominator(self) -> SupportsIndex: ...
    def __float__(self) -> float: ...

# See comment at the top of the file
# for why some of these return types are purposefully vague
class Integral(Rational):
    @abstractmethod
    def __int__(self) -> int: ...
    def __index__(self) -> int: ...
    @abstractmethod
    def __pow__(self, exponent: complex, modulus: int | None = None) -> SupportsIndex: ...  # type: ignore[override]
    @abstractmethod
    def __lshift__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __rlshift__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __rshift__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __rrshift__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __and__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __rand__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __xor__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __rxor__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __or__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __ror__(self, other: int) -> SupportsIndex: ...
    @abstractmethod
    def __invert__(self) -> SupportsIndex: ...
    def __float__(self) -> float: ...
    @property
    def numerator(self) -> SupportsIndex: ...
    @property
    def denominator(self) -> Literal[1]: ...
