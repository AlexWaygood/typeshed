import io
import os
from _typeshed import Incomplete, StrPath
from typing import AnyStr
from typing_extensions import TypeAlias

NativeIO: TypeAlias = io.StringIO

class Verifier:
    ffi: Incomplete
    preamble: Incomplete
    flags: int | None
    kwds: dict[str, list[str] | tuple[str]]
    tmpdir: StrPath
    sourcefilename: str
    modulefilename: str
    ext_package: str | None
    def __init__(
        self,
        ffi,
        preamble,
        tmpdir: StrPath | None = None,
        modulename: str | None = None,
        ext_package: str | None = None,
        tag: str = "",
        force_generic_engine: bool = False,
        source_extension: str = ".c",
        flags: int | None = None,
        relative_to: os.PathLike[AnyStr] | None = None,
        **kwds: list[str] | tuple[str],
    ) -> None: ...
    def write_source(self, file=None) -> None:
        """Write the C source code.  It is produced in 'self.sourcefilename',
        which can be tweaked beforehand.
        """

    def compile_module(self) -> None:
        """Write the C source code (if not done already) and compile it.
        This produces a dynamic link library in 'self.modulefilename'.
        """

    def load_library(self):
        """Get a C module from this Verifier instance.
        Returns an instance of a FFILibrary class that behaves like the
        objects returned by ffi.dlopen(), but that delegates all
        operations to the C module.  If necessary, the C code is written
        and compiled first.
        """

    def get_module_name(self) -> str: ...
    def get_extension(self): ...
    def generates_python_module(self) -> bool: ...
    def make_relative_to(
        self, kwds: dict[str, list[str] | tuple[str]], relative_to: os.PathLike[AnyStr] | None
    ) -> dict[str, list[str] | tuple[str]]: ...

def set_tmpdir(dirname: StrPath) -> None:
    """Set the temporary directory to use instead of __pycache__."""

def cleanup_tmpdir(tmpdir: StrPath | None = None, keep_so: bool = False) -> None:
    """Clean up the temporary directory by removing all files in it
    called `_cffi_*.{c,so}` as well as the `build` subdirectory.
    """
