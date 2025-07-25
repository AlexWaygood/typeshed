"""Provide access to Python's configuration information.  The specific
configuration variables available depend heavily on the platform and
configuration.  The values may be retrieved using
get_config_var(name), and the list of variables is available via
get_config_vars().keys().  Additional convenience functions are also
available.

Written by:   Fred L. Drake, Jr.
Email:        <fdrake@acm.org>
"""

from typing import Final, Literal, overload
from typing_extensions import deprecated

from setuptools._distutils.ccompiler import CCompiler

PREFIX: Final[str]
EXEC_PREFIX: Final[str]

@overload
@deprecated("SO is deprecated, use EXT_SUFFIX. Support will be removed when this module is synchronized with stdlib Python 3.11")
def get_config_var(name: Literal["SO"]) -> int | str | None:
    """Return the value of a single variable using the dictionary
    returned by 'get_config_vars()'.  Equivalent to
    get_config_vars().get(name)
    """

@overload
def get_config_var(name: str) -> int | str | None: ...
@overload
def get_config_vars() -> dict[str, str | int]:
    """With no arguments, return a dictionary of all configuration
    variables relevant for the current platform.  Generally this includes
    everything needed to build extensions and install both pure modules and
    extensions.  On Unix, this means every variable defined in Python's
    installed Makefile; on Windows it's a much smaller set.

    With arguments, return a list of values that result from looking up
    each argument in the configuration variable dictionary.
    """

@overload
def get_config_vars(arg: str, /, *args: str) -> list[str | int]: ...
def get_config_h_filename() -> str:
    """Return full pathname of installed pyconfig.h file."""

def get_makefile_filename() -> str:
    """Return full pathname of installed Makefile from the Python build."""

def get_python_inc(plat_specific: bool = False, prefix: str | None = None) -> str:
    """Return the directory containing installed Python header files.

    If 'plat_specific' is false (the default), this is the path to the
    non-platform-specific header files, i.e. Python.h and so on;
    otherwise, this is the path to platform-specific header files
    (namely pyconfig.h).

    If 'prefix' is supplied, use it instead of sys.base_prefix or
    sys.base_exec_prefix -- i.e., ignore 'plat_specific'.
    """

def get_python_lib(plat_specific: bool = False, standard_lib: bool = False, prefix: str | None = None) -> str:
    """Return the directory containing the Python library (standard or
    site additions).

    If 'plat_specific' is true, return the directory containing
    platform-specific modules, i.e. any module from a non-pure-Python
    module distribution; otherwise, return the platform-shared library
    directory.  If 'standard_lib' is true, return the directory
    containing standard Python library modules; otherwise, return the
    directory for site-specific modules.

    If 'prefix' is supplied, use it instead of sys.base_prefix or
    sys.base_exec_prefix -- i.e., ignore 'plat_specific'.
    """

def customize_compiler(compiler: CCompiler) -> None:
    """Do any platform-specific customization of a CCompiler instance.

    Mainly needed on Unix, so we can plug in the information that
    varies across Unices and is stored in Python's Makefile.
    """
