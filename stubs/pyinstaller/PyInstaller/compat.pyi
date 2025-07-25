"""
Various classes and functions to provide some backwards-compatibility with previous versions of Python onward.
"""

# https://pyinstaller.org/en/stable/hooks.html#module-PyInstaller.compat
from _typeshed import FileDescriptorOrPath
from collections.abc import Iterable
from types import ModuleType
from typing import Final, Literal, overload

strict_collect_mode: bool
is_64bits: Final[bool]
is_py35: Final = True
is_py36: Final = True
is_py37: Final = True
is_py38: Final = True
is_py39: Final[bool]
is_py310: Final[bool]
is_py311: Final[bool]
is_py312: Final[bool]
is_py313: Final[bool]
is_win: Final[bool]
is_win_10: Final[bool]
is_win_11: Final[bool]
is_win_wine: Final[bool]
is_cygwin: Final[bool]
is_darwin: Final[bool]
is_linux: Final[bool]
is_solar: Final[bool]
is_aix: Final[bool]
is_freebsd: Final[bool]
is_openbsd: Final[bool]
is_hpux: Final[bool]
is_unix: Final[bool]
is_musl: Final[bool]
is_termux: Final[bool]
is_macos_11_compat: Final[bool]
is_macos_11_native: Final[bool]
is_macos_11: Final[bool]
is_nogil: Final[bool]
PYDYLIB_NAMES: Final[set[str]]
base_prefix: Final[str]
is_venv: Final[bool]
is_virtualenv: Final[bool]
is_conda: Final[bool]
is_pure_conda: Final[bool]
python_executable: Final[str]
is_ms_app_store: Final[bool]
BYTECODE_MAGIC: Final[bytes]
EXTENSION_SUFFIXES: Final[list[str]]
ALL_SUFFIXES: Final[list[str]]

architecture: Final[Literal["64bit", "n32bit", "32bit"]]
system: Final[Literal["Cygwin", "Linux", "Darwin", "Java", "Windows"]]
machine: Final[
    Literal["AMD64", "x86", "ARM64", "sw_64", "loongarch64", "arm", "intel", "ppc", "mips", "riscv", "s390x", "unknown"] | None
]

def is_wine_dll(filename: FileDescriptorOrPath) -> bool:
    """
    Check if the given PE file is a Wine DLL (PE-converted built-in, or fake/placeholder one).

    Returns True if the given file is a Wine DLL, False if not (or if file cannot be analyzed or does not exist).
    """

@overload
def getenv(name: str, default: str) -> str:
    """
    Returns unicode string containing value of environment variable 'name'.
    """

@overload
def getenv(name: str, default: None = None) -> str | None: ...
def setenv(name: str, value: str) -> None:
    """
    Accepts unicode string and set it as environment variable 'name' containing value 'value'.
    """

def unsetenv(name: str) -> None:
    """
    Delete the environment variable 'name'.
    """

def exec_command(
    *cmdargs: str, encoding: str | None = None, raise_enoent: bool | None = None, **kwargs: int | bool | Iterable[int] | None
) -> str:
    """
    Run the command specified by the passed positional arguments, optionally configured by the passed keyword arguments.

    .. DANGER::
       **Ignore this function's return value** -- unless this command's standard output contains _only_ pathnames, in
       which case this function returns the correct filesystem-encoded string expected by PyInstaller. In all other
       cases, this function's return value is _not_ safely usable.

       For backward compatibility, this function's return value non-portably depends on the current Python version and
       passed keyword arguments:

       * Under Python 3.x, this value is a **decoded `str` string**. However, even this value is _not_ necessarily
         safely usable:
         * If the `encoding` parameter is passed, this value is guaranteed to be safely usable.
         * Else, this value _cannot_ be safely used for any purpose (e.g., string manipulation or parsing), except to be
           passed directly to another non-Python command. Why? Because this value has been decoded with the encoding
           specified by `sys.getfilesystemencoding()`, the encoding used by `os.fsencode()` and `os.fsdecode()` to
           convert from platform-agnostic to platform-specific pathnames. This is _not_ necessarily the encoding with
           which this command's standard output was encoded. Cue edge-case decoding exceptions.

    Parameters
    ----------
    cmdargs :
        Variadic list whose:
        1. Mandatory first element is the absolute path, relative path, or basename in the current `${PATH}` of the
           command to run.
        2. Optional remaining elements are arguments to pass to this command.
    encoding : str, optional
        Optional keyword argument specifying the encoding with which to decode this command's standard output under
        Python 3. As this function's return value should be ignored, this argument should _never_ be passed.
    raise_enoent : boolean, optional
        Optional keyword argument to simply raise the exception if the executing the command fails since to the command
        is not found. This is useful to checking id a command exists.

    All remaining keyword arguments are passed as is to the `subprocess.Popen()` constructor.

    Returns
    ----------
    str
        Ignore this value. See discussion above.
    """

def exec_command_rc(*cmdargs: str, **kwargs: float | bool | Iterable[int] | None) -> int:
    """
    Return the exit code of the command specified by the passed positional arguments, optionally configured by the
    passed keyword arguments.

    Parameters
    ----------
    cmdargs : list
        Variadic list whose:
        1. Mandatory first element is the absolute path, relative path, or basename in the current `${PATH}` of the
           command to run.
        2. Optional remaining elements are arguments to pass to this command.

    All keyword arguments are passed as is to the `subprocess.call()` function.

    Returns
    ----------
    int
        This command's exit code as an unsigned byte in the range `[0, 255]`, where 0 signifies success and all other
        values signal a failure.
    """

def exec_command_all(
    *cmdargs: str, encoding: str | None = None, **kwargs: int | bool | Iterable[int] | None
) -> tuple[int, str, str]:
    """
    Run the command specified by the passed positional arguments, optionally configured by the passed keyword arguments.

    .. DANGER::
       **Ignore this function's return value.** If this command's standard output consists solely of pathnames, consider
       calling `exec_command()`

    Parameters
    ----------
    cmdargs : str
        Variadic list whose:
        1. Mandatory first element is the absolute path, relative path, or basename in the current `${PATH}` of the
           command to run.
        2. Optional remaining elements are arguments to pass to this command.
    encoding : str, optional
        Optional keyword argument specifying the encoding with which to decode this command's standard output. As this
        function's return value should be ignored, this argument should _never_ be passed.

    All remaining keyword arguments are passed as is to the `subprocess.Popen()` constructor.

    Returns
    ----------
    (int, str, str)
        Ignore this 3-element tuple `(exit_code, stdout, stderr)`. See the `exec_command()` function for discussion.
    """

def exec_python(*args: str, **kwargs: str | None) -> str:
    """
    Wrap running python script in a subprocess.

    Return stdout of the invoked command.
    """

def exec_python_rc(*args: str, **kwargs: str | None) -> int:
    """
    Wrap running python script in a subprocess.

    Return exit code of the invoked command.
    """

def getsitepackages(prefixes: Iterable[str] | None = None) -> list[str]:
    """Returns a list containing all global site-packages directories.

    For each directory present in ``prefixes`` (or the global ``PREFIXES``),
    this function will find its `site-packages` subdirectory depending on the
    system environment, and will return a list of full paths.
    """

def importlib_load_source(name: str, pathname: str) -> ModuleType: ...

PY3_BASE_MODULES: Final[set[str]]
PURE_PYTHON_MODULE_TYPES: Final[set[str]]
SPECIAL_MODULE_TYPES: Final[set[str]]
BINARY_MODULE_TYPES: Final[set[str]]
VALID_MODULE_TYPES: Final[set[str]]
BAD_MODULE_TYPES: Final[set[str]]
ALL_MODULE_TYPES: Final[set[str]]
MODULE_TYPES_TO_TOC_DICT: Final[dict[str, str]]

def check_requirements() -> None:
    """
    Verify that all requirements to run PyInstaller are met.

    Fail hard if any requirement is not met.
    """
