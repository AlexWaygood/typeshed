"""
General helpers required for `tqdm.std`.
"""

from _typeshed import Incomplete
from collections.abc import Callable, Mapping
from re import Pattern
from typing import Protocol, TypeVar
from typing_extensions import ParamSpec

CUR_OS: str
IS_WIN: bool
IS_NIX: bool
RE_ANSI: Pattern[str]

class FormatReplace:
    """
    >>> a = FormatReplace('something')
    >>> f"{a:5d}"
    'something'
    """

    replace: str
    format_called: int
    def __init__(self, replace: str = "") -> None: ...
    def __format__(self, _) -> str: ...

class _Has__Comparable(Protocol):
    _comparable: Incomplete

class Comparable:
    """Assumes child has self._comparable attr/@property"""

    _comparable: Incomplete
    def __lt__(self, other: _Has__Comparable) -> bool: ...
    def __le__(self, other: _Has__Comparable) -> bool: ...
    def __eq__(self, other: _Has__Comparable) -> bool: ...  # type: ignore[override]
    def __ne__(self, other: _Has__Comparable) -> bool: ...  # type: ignore[override]
    def __gt__(self, other: _Has__Comparable) -> bool: ...
    def __ge__(self, other: _Has__Comparable) -> bool: ...

class ObjectWrapper:
    def __getattr__(self, name: str): ...
    def __setattr__(self, name: str, value) -> None: ...
    def wrapper_getattr(self, name):
        """Actual `self.getattr` rather than self._wrapped.getattr"""

    def wrapper_setattr(self, name, value):
        """Actual `self.setattr` rather than self._wrapped.setattr"""

    def __init__(self, wrapped) -> None:
        """
        Thin wrapper around a given object
        """

class SimpleTextIOWrapper(ObjectWrapper):
    """
    Change only `.write()` of the wrapped object by encoding the passed
    value and passing the result to the wrapped object's `.write()` method.
    """

    def __init__(self, wrapped, encoding) -> None: ...
    def write(self, s: str):
        """
        Encode `s` and pass to the wrapped object's `.write()` method.
        """

    def __eq__(self, other: object) -> bool: ...

_P = ParamSpec("_P")
_R = TypeVar("_R")

class DisableOnWriteError(ObjectWrapper):
    """
    Disable the given `tqdm_instance` upon `write()` or `flush()` errors.
    """

    @staticmethod
    def disable_on_exception(tqdm_instance, func: Callable[_P, _R]) -> Callable[_P, _R]:
        """
        Quietly set `tqdm_instance.miniters=inf` if `func` raises `errno=5`.
        """

    def __init__(self, wrapped, tqdm_instance) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class CallbackIOWrapper(ObjectWrapper):
    def __init__(self, callback: Callable[[int], object], stream, method: str = "read") -> None:
        """
        Wrap a given `file`-like object's `read()` or `write()` to report
        lengths to the given `callback`
        """

def disp_len(data: str) -> int:
    """
    Returns the real on-screen length of a string which may contain
    ANSI control codes and wide chars.
    """

def disp_trim(data: str, length: int) -> str:
    """
    Trim a string which may contain ANSI control characters.
    """

def envwrap(
    prefix: str, types: Mapping[str, Callable[[Incomplete], Incomplete]] | None = None, is_method: bool = False
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """
    Override parameter defaults via `os.environ[prefix + param_name]`.
    Maps UPPER_CASE env vars map to lower_case param names.
    camelCase isn't supported (because Windows ignores case).

    Precedence (highest first):

    - call (`foo(a=3)`)
    - environ (`FOO_A=2`)
    - signature (`def foo(a=1)`)

    Parameters
    ----------
    prefix  : str
        Env var prefix, e.g. "FOO_"
    types  : dict, optional
        Fallback mappings `{'param_name': type, ...}` if types cannot be
        inferred from function signature.
        Consider using `types=collections.defaultdict(lambda: ast.literal_eval)`.
    is_method  : bool, optional
        Whether to use `functools.partialmethod`. If (default: False) use `functools.partial`.

    Examples
    --------
    ```
    $ cat foo.py
    from tqdm.utils import envwrap
    @envwrap("FOO_")
    def test(a=1, b=2, c=3):
        print(f"received: a={a}, b={b}, c={c}")

    $ FOO_A=42 FOO_C=1337 python -c 'import foo; foo.test(c=99)'
    received: a=42, b=2, c=99
    ```
    """
