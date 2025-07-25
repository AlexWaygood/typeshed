from _typeshed import StrPath
from collections.abc import Iterable

from ._distutils.extension import Extension as _Extension

def have_pyrex() -> bool:
    """
    Return True if Cython can be imported.
    """

class Extension(_Extension):
    """
    Describes a single extension module.

    This means that all source files will be compiled into a single binary file
    ``<module path>.<suffix>`` (with ``<module path>`` derived from ``name`` and
    ``<suffix>`` defined by one of the values in
    ``importlib.machinery.EXTENSION_SUFFIXES``).

    In the case ``.pyx`` files are passed as ``sources and`` ``Cython`` is **not**
    installed in the build environment, ``setuptools`` may also try to look for the
    equivalent ``.cpp`` or ``.c`` files.

    :arg str name:
      the full name of the extension, including any packages -- ie.
      *not* a filename or pathname, but Python dotted name

    :arg list[str|os.PathLike[str]] sources:
      list of source filenames, relative to the distribution root
      (where the setup script lives), in Unix form (slash-separated)
      for portability.  Source files may be C, C++, SWIG (.i),
      platform-specific resource files, or whatever else is recognized
      by the "build_ext" command as source for a Python extension.

    :keyword list[str] include_dirs:
      list of directories to search for C/C++ header files (in Unix
      form for portability)

    :keyword list[tuple[str, str|None]] define_macros:
      list of macros to define; each macro is defined using a 2-tuple:
      the first item corresponding to the name of the macro and the second
      item either a string with its value or None to
      define it without a particular value (equivalent of "#define
      FOO" in source or -DFOO on Unix C compiler command line)

    :keyword list[str] undef_macros:
      list of macros to undefine explicitly

    :keyword list[str] library_dirs:
      list of directories to search for C/C++ libraries at link time

    :keyword list[str] libraries:
      list of library names (not filenames or paths) to link against

    :keyword list[str] runtime_library_dirs:
      list of directories to search for C/C++ libraries at run time
      (for shared extensions, this is when the extension is loaded).
      Setting this will cause an exception during build on Windows
      platforms.

    :keyword list[str] extra_objects:
      list of extra files to link with (eg. object files not implied
      by 'sources', static library that must be explicitly specified,
      binary resource files, etc.)

    :keyword list[str] extra_compile_args:
      any extra platform- and compiler-specific information to use
      when compiling the source files in 'sources'.  For platforms and
      compilers where "command line" makes sense, this is typically a
      list of command-line arguments, but for other platforms it could
      be anything.

    :keyword list[str] extra_link_args:
      any extra platform- and compiler-specific information to use
      when linking object files together to create the extension (or
      to create a new static Python interpreter).  Similar
      interpretation as for 'extra_compile_args'.

    :keyword list[str] export_symbols:
      list of symbols to be exported from a shared extension.  Not
      used on all platforms, and not generally necessary for Python
      extensions, which typically export exactly one symbol: "init" +
      extension_name.

    :keyword list[str] swig_opts:
      any extra options to pass to SWIG if a source file has the .i
      extension.

    :keyword list[str] depends:
      list of files that the extension depends on

    :keyword str language:
      extension language (i.e. "c", "c++", "objc"). Will be detected
      from the source extensions if not provided.

    :keyword bool optional:
      specifies that a build failure in the extension should not abort the
      build process, but simply not install the failing extension.

    :keyword bool py_limited_api:
      opt-in flag for the usage of :doc:`Python's limited API <python:c-api/stable>`.

    :raises setuptools.errors.PlatformError: if ``runtime_library_dirs`` is
      specified on Windows. (since v63)
    """

    py_limited_api: bool
    def __init__(
        self,
        name: str,
        sources: Iterable[StrPath],
        include_dirs: list[str] | None = None,
        define_macros: list[tuple[str, str | None]] | None = None,
        undef_macros: list[str] | None = None,
        library_dirs: list[str] | None = None,
        libraries: list[str] | None = None,
        runtime_library_dirs: list[str] | None = None,
        extra_objects: list[str] | None = None,
        extra_compile_args: list[str] | None = None,
        extra_link_args: list[str] | None = None,
        export_symbols: list[str] | None = None,
        swig_opts: list[str] | None = None,
        depends: list[str] | None = None,
        language: str | None = None,
        optional: bool | None = None,
        *,
        py_limited_api: bool = False,
    ) -> None: ...

class Library(Extension):
    """Just like a regular Extension, but built as a library instead"""
