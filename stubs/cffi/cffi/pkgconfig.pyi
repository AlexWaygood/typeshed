from collections.abc import Sequence

def merge_flags(cfg1: dict[str, list[str]], cfg2: dict[str, list[str]]) -> dict[str, list[str]]:
    """Merge values from cffi config flags cfg2 to cf1

    Example:
        merge_flags({"libraries": ["one"]}, {"libraries": ["two"]})
        {"libraries": ["one", "two"]}
    """

def call(libname: str, flag: str, encoding: str = ...) -> str:
    """Calls pkg-config and returns the output if found"""

def flags_from_pkgconfig(libs: Sequence[str]) -> dict[str, list[str]]:
    """Return compiler line flags for FFI.set_source based on pkg-config output

    Usage
        ...
        ffibuilder.set_source("_foo", pkgconfig = ["libfoo", "libbar >= 1.8.3"])

    If pkg-config is installed on build machine, then arguments include_dirs,
    library_dirs, libraries, define_macros, extra_compile_args and
    extra_link_args are extended with an output of pkg-config for libfoo and
    libbar.

    Raises PkgConfigError in case the pkg-config call fails.
    """
