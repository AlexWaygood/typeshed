"""distutils.unixccompiler

Contains the UnixCCompiler class, a subclass of CCompiler that handles
the "typical" Unix-style command-line C compiler:
  * macros defined with -Dname[=value]
  * macros undefined with -Uname
  * include search directories specified with -Idir
  * libraries specified with -lllib
  * library search directories specified with -Ldir
  * compile handled by 'cc' (or similar) executable with -c option:
    compiles .c to .o
  * link static library handled by 'ar' command (possibly with 'ranlib')
  * link shared library handled by 'cc -shared'
"""

from typing import ClassVar

from . import base

class Compiler(base.Compiler):
    src_extensions: ClassVar[list[str]]
    obj_extension: ClassVar[str]
    static_lib_extension: ClassVar[str]
    shared_lib_extension: ClassVar[str]
    dylib_lib_extension: ClassVar[str]
    xcode_stub_lib_extension: ClassVar[str]
    static_lib_format: ClassVar[str]
    shared_lib_format: ClassVar[str]
    dylib_lib_format: ClassVar[str]
    xcode_stub_lib_format: ClassVar[str]
    def runtime_library_dir_option(self, dir: str) -> str | list[str]: ...  # type: ignore[override]
