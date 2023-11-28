import sys
from _typeshed import structseq
from collections.abc import AsyncGenerator, Callable
from typing import Any
from typing_extensions import Literal, TypeAlias, final

# Type alias used as a mixin for structseq classes that cannot be instantiated at runtime
# This can't be represented in the type system, so we just use `structseq[Any]`
_UninstantiableStructseq: TypeAlias = structseq[Any]

flags: _flags
_FlagTuple: TypeAlias = tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, bool, int, int]

@final
class _flags(_UninstantiableStructseq, _FlagTuple):
    @property
    def debug(self) -> int: ...
    @property
    def inspect(self) -> int: ...
    @property
    def interactive(self) -> int: ...
    @property
    def optimize(self) -> int: ...
    @property
    def dont_write_bytecode(self) -> int: ...
    @property
    def no_user_site(self) -> int: ...
    @property
    def no_site(self) -> int: ...
    @property
    def ignore_environment(self) -> int: ...
    @property
    def verbose(self) -> int: ...
    @property
    def bytes_warning(self) -> int: ...
    @property
    def quiet(self) -> int: ...
    @property
    def hash_randomization(self) -> int: ...
    @property
    def isolated(self) -> int: ...
    @property
    def dev_mode(self) -> bool: ...
    @property
    def utf8_mode(self) -> int: ...
    if sys.version_info >= (3, 10):
        @property
        def warn_default_encoding(self) -> int: ...  # undocumented
    if sys.version_info >= (3, 11):
        @property
        def safe_path(self) -> bool: ...

float_info: _float_info

@final
class _float_info(structseq[float], tuple[float, int, int, float, int, int, int, int, float, int, int]):
    @property
    def max(self) -> float: ...  # DBL_MAX
    @property
    def max_exp(self) -> int: ...  # DBL_MAX_EXP
    @property
    def max_10_exp(self) -> int: ...  # DBL_MAX_10_EXP
    @property
    def min(self) -> float: ...  # DBL_MIN
    @property
    def min_exp(self) -> int: ...  # DBL_MIN_EXP
    @property
    def min_10_exp(self) -> int: ...  # DBL_MIN_10_EXP
    @property
    def dig(self) -> int: ...  # DBL_DIG
    @property
    def mant_dig(self) -> int: ...  # DBL_MANT_DIG
    @property
    def epsilon(self) -> float: ...  # DBL_EPSILON
    @property
    def radix(self) -> int: ...  # FLT_RADIX
    @property
    def rounds(self) -> int: ...  # FLT_ROUNDS

hash_info: _hash_info

@final
class _hash_info(structseq[Any | int], tuple[int, int, int, int, int, str, int, int, int]):
    @property
    def width(self) -> int: ...
    @property
    def modulus(self) -> int: ...
    @property
    def inf(self) -> int: ...
    @property
    def nan(self) -> int: ...
    @property
    def imag(self) -> int: ...
    @property
    def algorithm(self) -> str: ...
    @property
    def hash_bits(self) -> int: ...
    @property
    def seed_bits(self) -> int: ...
    @property
    def cutoff(self) -> int: ...  # undocumented

implementation: _implementation

class _implementation:
    name: str
    version: _version_info
    hexversion: int
    cache_tag: str
    # Define __getattr__, as the documentation states:
    # > sys.implementation may contain additional attributes specific to the Python implementation.
    # > These non-standard attributes must start with an underscore, and are not described here.
    def __getattr__(self, name: str) -> Any: ...

int_info: _int_info

@final
class _int_info(structseq[int], tuple[int, int, int, int]):
    @property
    def bits_per_digit(self) -> int: ...
    @property
    def sizeof_digit(self) -> int: ...
    @property
    def default_max_str_digits(self) -> int: ...
    @property
    def str_digits_check_threshold(self) -> int: ...

_ThreadInfoName: TypeAlias = Literal["nt", "pthread", "pthread-stubs", "solaris"]
_ThreadInfoLock: TypeAlias = Literal["semaphore", "mutex+cond"] | None

@final
class _thread_info(_UninstantiableStructseq, tuple[_ThreadInfoName, _ThreadInfoLock, str | None]):
    @property
    def name(self) -> _ThreadInfoName: ...
    @property
    def lock(self) -> _ThreadInfoLock: ...
    @property
    def version(self) -> str | None: ...

thread_info: _thread_info
_ReleaseLevel: TypeAlias = Literal["alpha", "beta", "candidate", "final"]

@final
class _version_info(_UninstantiableStructseq, tuple[int, int, int, _ReleaseLevel, int]):
    @property
    def major(self) -> int: ...
    @property
    def minor(self) -> int: ...
    @property
    def micro(self) -> int: ...
    @property
    def releaselevel(self) -> _ReleaseLevel: ...
    @property
    def serial(self) -> int: ...

version_info: _version_info

_AsyncgenHook: TypeAlias = Callable[[AsyncGenerator[Any, Any]], None] | None

@final
class _asyncgen_hooks(structseq[_AsyncgenHook], tuple[_AsyncgenHook, _AsyncgenHook]):
    @property
    def firstiter(self) -> _AsyncgenHook: ...
    @property
    def finalizer(self) -> _AsyncgenHook: ...
