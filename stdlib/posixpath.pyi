import sys
from _typeshed import AnyOrLiteralStr, BytesPath, FileDescriptorOrPath, StrOrBytesPath, StrPath
from collections.abc import Iterable
from genericpath import (
    commonprefix as commonprefix,
    exists as exists,
    getatime as getatime,
    getctime as getctime,
    getmtime as getmtime,
    getsize as getsize,
    isdir as isdir,
    isfile as isfile,
    samefile as samefile,
    sameopenfile as sameopenfile,
    samestat as samestat,
)

if sys.version_info >= (3, 13):
    from genericpath import isdevdrive as isdevdrive
from os import PathLike
from typing import AnyStr, overload
from typing_extensions import LiteralString

__all__ = [
    "normcase",
    "isabs",
    "join",
    "splitdrive",
    "split",
    "splitext",
    "basename",
    "dirname",
    "commonprefix",
    "getsize",
    "getmtime",
    "getatime",
    "getctime",
    "islink",
    "exists",
    "lexists",
    "isdir",
    "isfile",
    "ismount",
    "expanduser",
    "expandvars",
    "normpath",
    "abspath",
    "samefile",
    "sameopenfile",
    "samestat",
    "curdir",
    "pardir",
    "sep",
    "pathsep",
    "defpath",
    "altsep",
    "extsep",
    "devnull",
    "realpath",
    "supports_unicode_filenames",
    "relpath",
    "commonpath",
]
if sys.version_info >= (3, 12):
    __all__ += ["isjunction", "splitroot"]
if sys.version_info >= (3, 13):
    __all__ += ["isdevdrive"]

supports_unicode_filenames: bool
# aliases (also in os)
curdir: LiteralString
pardir: LiteralString
sep: LiteralString
altsep: LiteralString | None
extsep: LiteralString
pathsep: LiteralString
defpath: LiteralString
devnull: LiteralString

# Overloads are necessary to work around python/mypy#17952 & python/mypy#11880
@overload
def abspath[AnyStr: (bytes, str)](path: PathLike[AnyStr]) -> AnyStr: ...
@overload
def abspath[AnyStr: (bytes, str)](path: AnyStr) -> AnyStr: ...
@overload
def basename[AnyStr: (bytes, str)](p: PathLike[AnyStr]) -> AnyStr: ...
@overload
def basename(p: AnyOrLiteralStr) -> AnyOrLiteralStr: ...
@overload
def dirname[AnyStr: (bytes, str)](p: PathLike[AnyStr]) -> AnyStr: ...
@overload
def dirname(p: AnyOrLiteralStr) -> AnyOrLiteralStr: ...
@overload
def expanduser[AnyStr: (bytes, str)](path: PathLike[AnyStr]) -> AnyStr: ...
@overload
def expanduser[AnyStr: (bytes, str)](path: AnyStr) -> AnyStr: ...
@overload
def expandvars[AnyStr: (bytes, str)](path: PathLike[AnyStr]) -> AnyStr: ...
@overload
def expandvars[AnyStr: (bytes, str)](path: AnyStr) -> AnyStr: ...
@overload
def normcase[AnyStr: (bytes, str)](s: PathLike[AnyStr]) -> AnyStr: ...
@overload
def normcase(s: AnyOrLiteralStr) -> AnyOrLiteralStr: ...
@overload
def normpath[AnyStr: (bytes, str)](path: PathLike[AnyStr]) -> AnyStr: ...
@overload
def normpath(path: AnyOrLiteralStr) -> AnyOrLiteralStr: ...
@overload
def commonpath(paths: Iterable[LiteralString]) -> LiteralString: ...
@overload
def commonpath(paths: Iterable[StrPath]) -> str: ...
@overload
def commonpath(paths: Iterable[BytesPath]) -> bytes: ...

# First parameter is not actually pos-only,
# but must be defined as pos-only in the stub or cross-platform code doesn't type-check,
# as the parameter name is different in ntpath.join()
@overload
def join(a: LiteralString, /, *paths: LiteralString) -> LiteralString: ...
@overload
def join(a: StrPath, /, *paths: StrPath) -> str: ...
@overload
def join(a: BytesPath, /, *paths: BytesPath) -> bytes: ...

if sys.version_info >= (3, 10):
    @overload
    def realpath[AnyStr: (bytes, str)](filename: PathLike[AnyStr], *, strict: bool = False) -> AnyStr: ...
    @overload
    def realpath[AnyStr: (bytes, str)](filename: AnyStr, *, strict: bool = False) -> AnyStr: ...

else:
    @overload
    def realpath[AnyStr: (bytes, str)](filename: PathLike[AnyStr]) -> AnyStr: ...
    @overload
    def realpath[AnyStr: (bytes, str)](filename: AnyStr) -> AnyStr: ...

@overload
def relpath(path: LiteralString, start: LiteralString | None = None) -> LiteralString: ...
@overload
def relpath(path: BytesPath, start: BytesPath | None = None) -> bytes: ...
@overload
def relpath(path: StrPath, start: StrPath | None = None) -> str: ...
@overload
def split[AnyStr: (bytes, str)](p: PathLike[AnyStr]) -> tuple[AnyStr, AnyStr]: ...
@overload
def split(p: AnyOrLiteralStr) -> tuple[AnyOrLiteralStr, AnyOrLiteralStr]: ...
@overload
def splitdrive[AnyStr: (bytes, str)](p: PathLike[AnyStr]) -> tuple[AnyStr, AnyStr]: ...
@overload
def splitdrive(p: AnyOrLiteralStr) -> tuple[AnyOrLiteralStr, AnyOrLiteralStr]: ...
@overload
def splitext[AnyStr: (bytes, str)](p: PathLike[AnyStr]) -> tuple[AnyStr, AnyStr]: ...
@overload
def splitext(p: AnyOrLiteralStr) -> tuple[AnyOrLiteralStr, AnyOrLiteralStr]: ...
def isabs(s: StrOrBytesPath) -> bool: ...
def islink(path: FileDescriptorOrPath) -> bool: ...
def ismount(path: FileDescriptorOrPath) -> bool: ...
def lexists(path: FileDescriptorOrPath) -> bool: ...

if sys.version_info >= (3, 12):
    def isjunction(path: StrOrBytesPath) -> bool: ...
    @overload
    def splitroot(p: AnyOrLiteralStr) -> tuple[AnyOrLiteralStr, AnyOrLiteralStr, AnyOrLiteralStr]: ...
    @overload
    def splitroot[AnyStr: (bytes, str)](p: PathLike[AnyStr]) -> tuple[AnyStr, AnyStr, AnyStr]: ...
