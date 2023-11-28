from _typeshed import structseq
from typing import Any
from typing_extensions import Literal, TypeAlias, final

# Type alias used as a mixin for structseq classes that cannot be instantiated at runtime
# This can't be represented in the type system, so we just use `structseq[Any]`
_UninstantiableStructseq: TypeAlias = structseq[Any]

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
