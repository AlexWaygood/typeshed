# Note: these stubs are incomplete. The more complex type
# signatures are currently omitted.
#
# Use _ComplexLike, _RealLike and _IntegralLike for return types in this module
# rather than `numbers.Complex`, `numbers.Real` and `numbers.Integral`,
# to avoid an excessive number of `type: ignore`s in subclasses of these ABCs
# (since type checkers don't see `complex` as a subtype of `numbers.Complex`,
# nor `float` as a subtype of `numbers.Real`, etc.)

import sys
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from typing import Literal, Protocol, overload
from typing_extensions import TypeAlias

__all__ = ["Number", "Complex", "Real", "Rational", "Integral"]

############################
# Protocols for return types
############################

# `_ComplexLike` is a structural-typing approximation
# of the `Complex` ABC, which is not (and cannot be) a protocol
class _SupportsComplex(Protocol):
    def __complex__(self) -> complex: ...
    def __abs__(self) -> _RealLike: ...
    def __neg__(self) -> _ComplexLike: ...
    def __pos__(self) -> _ComplexLike: ...

if sys.version_info >= (3, 11):
    _ComplexLike: TypeAlias = _SupportsComplex
else:
    # builtins.complex didn't have a __complex__ method on older Pythons
    _ComplexLike: TypeAlias = _SupportsComplex | complex

# _RealLike is a structural-typing approximation
# of the `Real` ABC, which is not (and cannot be) a protocol
#
# NOTE: _RealLike can't inherit from _SupportsComplex,
# because not all builtin types that we want to be understood
# as subtypes of _RealLike have a `__complex__` method
# (e.g. `builtins.int.__complex__` does not exist)
class _RealLike(Protocol):
    def __neg__(self) -> _ComplexLike: ...  # TODO: ideally would be more precise
    def __pos__(self) -> _ComplexLike: ...  # TODO: ideally would be more precise
    def __abs__(self) -> _RealLike: ...
    def __float__(self) -> float: ...
    def __trunc__(self) -> _IntegralLike: ...
    def __floor__(self) -> _IntegralLike: ...
    def __ceil__(self) -> _IntegralLike: ...

# _IntegralLike is a structural-typing approximation
# of the `Integral` ABC, which is not (and cannot be) a protocol
class _IntegralLike(_RealLike, Protocol):
    def __int__(self) -> int: ...
    def __index__(self) -> int: ...
    def __invert__(self) -> _IntegralLike: ...
    def __abs__(self) -> _IntegralLike: ...

#################
# Module "proper"
#################

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
    def real(self) -> _RealLike: ...
    @property
    @abstractmethod
    def imag(self) -> _RealLike: ...
    @abstractmethod
    def __add__(self, other) -> _ComplexLike: ...
    @abstractmethod
    def __radd__(self, other) -> _ComplexLike: ...
    @abstractmethod
    def __neg__(self) -> _ComplexLike: ...
    @abstractmethod
    def __pos__(self) -> _ComplexLike: ...
    def __sub__(self, other) -> _ComplexLike: ...
    def __rsub__(self, other) -> _ComplexLike: ...
    @abstractmethod
    def __mul__(self, other) -> _ComplexLike: ...
    @abstractmethod
    def __rmul__(self, other) -> _ComplexLike: ...
    @abstractmethod
    def __truediv__(self, other) -> _ComplexLike: ...
    @abstractmethod
    def __rtruediv__(self, other) -> _ComplexLike: ...
    @abstractmethod
    def __pow__(self, exponent) -> _ComplexLike: ...
    @abstractmethod
    def __rpow__(self, base) -> _ComplexLike: ...
    @abstractmethod
    def __abs__(self) -> _RealLike: ...
    @abstractmethod
    def conjugate(self) -> _ComplexLike: ...
    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

# See comment at the top of the file
# for why some of these return types are purposefully vague
class Real(Complex):
    @abstractmethod
    def __float__(self) -> float: ...
    @abstractmethod
    def __trunc__(self) -> _IntegralLike: ...
    @abstractmethod
    def __floor__(self) -> _IntegralLike: ...
    @abstractmethod
    def __ceil__(self) -> _IntegralLike: ...
    @abstractmethod
    @overload
    def __round__(self, ndigits: None = None) -> _IntegralLike: ...
    @abstractmethod
    @overload
    def __round__(self, ndigits: int) -> _RealLike: ...
    def __divmod__(self, other) -> tuple[_RealLike, _RealLike]: ...
    def __rdivmod__(self, other) -> tuple[_RealLike, _RealLike]: ...
    @abstractmethod
    def __floordiv__(self, other) -> _RealLike: ...
    @abstractmethod
    def __rfloordiv__(self, other) -> _RealLike: ...
    @abstractmethod
    def __mod__(self, other) -> _RealLike: ...
    @abstractmethod
    def __rmod__(self, other) -> _RealLike: ...
    @abstractmethod
    def __lt__(self, other) -> bool: ...
    @abstractmethod
    def __le__(self, other) -> bool: ...
    def __complex__(self) -> complex: ...
    @property
    def real(self) -> _RealLike: ...
    @property
    def imag(self) -> Literal[0]: ...
    def conjugate(self) -> _RealLike: ...  # type: ignore[override]

# See comment at the top of the file
# for why some of these return types are purposefully vague
class Rational(Real):
    @property
    @abstractmethod
    def numerator(self) -> _IntegralLike: ...
    @property
    @abstractmethod
    def denominator(self) -> _IntegralLike: ...
    def __float__(self) -> float: ...

# See comment at the top of the file
# for why some of these return types are purposefully vague
class Integral(Rational):
    @abstractmethod
    def __int__(self) -> int: ...
    def __index__(self) -> int: ...
    @abstractmethod
    def __pow__(self, exponent, modulus: Incomplete | None = None) -> _IntegralLike: ...  # type: ignore[override]
    @abstractmethod
    def __lshift__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __rlshift__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __rshift__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __rrshift__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __and__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __rand__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __xor__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __rxor__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __or__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __ror__(self, other) -> _IntegralLike: ...
    @abstractmethod
    def __invert__(self) -> _IntegralLike: ...
    def __float__(self) -> float: ...
    @property
    def numerator(self) -> _IntegralLike: ...
    @property
    def denominator(self) -> Literal[1]: ...
    # Not actually overridden at runtime,
    # but we override it in the stub to give it a more precise return type:
    @abstractmethod
    def __abs__(self) -> _IntegralLike: ...
