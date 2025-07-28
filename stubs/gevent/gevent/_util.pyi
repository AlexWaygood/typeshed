"""
internal gevent utilities, not for external use.
"""

from collections.abc import Callable, Iterable, MutableMapping, Sequence
from types import ModuleType
from typing import Any, Generic, TypeVar, overload
from typing_extensions import Self

_T = TypeVar("_T")

WRAPPER_ASSIGNMENTS: tuple[str, ...]
WRAPPER_UPDATES: tuple[str, ...]

def update_wrapper(wrapper: _T, wrapped: object, assigned: Sequence[str] = ..., updated: Sequence[str] = ...) -> _T:
    """
    Based on code from the standard library ``functools``, but
    doesn't perform any of the troublesome imports.

    functools imports RLock from _thread for purposes of the
    ``lru_cache``, making it problematic to use from gevent.

    The other imports are somewhat heavy: abc, collections, types.
    """

def copy_globals(
    source: ModuleType,
    globs: MutableMapping[str, Any],
    only_names: Iterable[str] | None = None,
    ignore_missing_names: bool = False,
    names_to_ignore: Sequence[str] = ...,
    dunder_names_to_keep: Sequence[str] = ...,
    cleanup_globs: bool = True,
) -> list[str]:
    """
    Copy attributes defined in ``source.__dict__`` to the dictionary
    in globs (which should be the caller's :func:`globals`).

    Names that start with ``__`` are ignored (unless they are in
    *dunder_names_to_keep*). Anything found in *names_to_ignore* is
    also ignored.

    If *only_names* is given, only those attributes will be
    considered. In this case, *ignore_missing_names* says whether or
    not to raise an :exc:`AttributeError` if one of those names can't
    be found.

    If *cleanup_globs* has a true value, then common things imported but
    not used at runtime are removed, including this function.

    Returns a list of the names copied; this should be assigned to ``__imports__``.
    """

def import_c_accel(globs: MutableMapping[str, Any], cname: str) -> None:
    """
    Import the C-accelerator for the *cname*
    and copy its globals.

    The *cname* should be hardcoded to match the expected
    C accelerator module.

    Unless PURE_PYTHON is set (in the environment or automatically
    on PyPy), then the C-accelerator is required.
    """

class Lazy(Generic[_T]):
    """
    A non-data descriptor used just like @property. The
    difference is the function value is assigned to the instance
    dict the first time it is accessed and then the function is never
    called again.

    Contrast with `readproperty`.
    """

    data: _T
    def __init__(self, func: Callable[[Any], _T]) -> None: ...
    @overload
    def __get__(self, inst: None, class_: type[object]) -> Self: ...
    @overload
    def __get__(self, inst: object, class_: type[object]) -> _T: ...

class readproperty(Generic[_T]):
    """
    A non-data descriptor similar to :class:`property`.

    The difference is that the property can be assigned to directly,
    without invoking a setter function. When the property is assigned
    to, it is cached in the instance and the function is not called on
    that instance again.

    Contrast with `Lazy`, which caches the result of the function in the
    instance the first time it is called and never calls the function on that
    instance again.
    """

    func: Callable[[Any], _T]
    def __init__(
        self: readproperty[_T], func: Callable[[Any], _T]  # pyright: ignore[reportInvalidTypeVarUse]  #11780
    ) -> None: ...
    @overload
    def __get__(self, inst: None, class_: type[object]) -> Self: ...
    @overload
    def __get__(self, inst: object, class_: type[object]) -> _T: ...

class LazyOnClass(Generic[_T]):
    """
    Similar to `Lazy`, but stores the value in the class.

    This is useful when the getter is expensive and conceptually
    a shared class value, but we don't want import-time side-effects
    such as expensive imports because it may not always be used.

    Probably doesn't mix well with inheritance?
    """

    @classmethod
    def lazy(cls, cls_dict: MutableMapping[str, Any], func: Callable[[Any], _T]) -> None:
        """Put a LazyOnClass object in *cls_dict* with the same name as *func*"""
    name: str
    func: Callable[[Any], _T]
    def __init__(self, func: Callable[[Any], _T], name: str | None = None) -> None: ...
    @overload
    def __get__(self, inst: None, class_: type[object]) -> Self: ...
    @overload
    def __get__(self, inst: object, class_: type[object]) -> _T: ...

def gmctime() -> str:
    """
    Returns the current time as a string in RFC3339 format.
    """

def prereleaser_middle(data: MutableMapping[str, Any]) -> None:
    """
    zest.releaser prerelease middle hook for gevent.

    The prerelease step:

        asks you for a version number
        updates the setup.py or version.txt and the
        CHANGES/HISTORY/CHANGELOG file (with either
        this new version
        number and offers to commit those changes to git

    The middle hook:

        All data dictionary items are available and some questions
        (like new version number) have been asked.
        No filesystem changes have been made yet.

    It is our job to finish up the filesystem changes needed, including:

    - Calling towncrier to handle CHANGES.rst
    - Add the version number to ``versionadded``, ``versionchanged`` and
      ``deprecated`` directives in Python source.
    """

def postreleaser_before(data: MutableMapping[str, Any]) -> None:
    """
    Prevents zest.releaser from modifying the CHANGES.rst to add the
    'no changes yet' section; towncrier is in charge of CHANGES.rst.

    Needs zest.releaser 6.15.0.
    """
