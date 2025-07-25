"""Decorators for Shapely functions."""

from collections.abc import Callable, Container
from typing import TypeVar

_F = TypeVar("_F", bound=Callable[..., object])

class requires_geos:
    """Decorator to require a minimum GEOS version."""

    version: tuple[int, int, int]
    def __init__(self, version: str) -> None:
        """Create a decorator that requires a minimum GEOS version."""

    def __call__(self, func: _F) -> _F:
        """Return the wrapped function."""

def multithreading_enabled(func: _F) -> _F:
    """Enable multithreading.

    To do this, the writable flags of object type ndarrays are set to False.

    NB: multithreading also requires the GIL to be released, which is done in
    the C extension (ufuncs.c).
    """

def deprecate_positional(should_be_kwargs: Container[str], category: type[Warning] = ...) -> Callable[..., object]:
    """Show warning if positional arguments are used that should be keyword.

    Parameters
    ----------
    should_be_kwargs : Iterable[str]
        Names of parameters that should be passed as keyword arguments.
    category : type[Warning], optional (default: DeprecationWarning)
        Warning category to use for deprecation warnings.

    Returns
    -------
    callable
        Decorator function that adds positional argument deprecation warnings.

    Examples
    --------
    >>> from shapely.decorators import deprecate_positional
    >>> @deprecate_positional(['b', 'c'])
    ... def example(a, b, c=None):
    ...     return a, b, c
    ...
    >>> example(1, 2)  # doctest: +SKIP
    DeprecationWarning: positional argument `b` for `example` is deprecated. ...
    (1, 2, None)
    >>> example(1, b=2)  # No warnings
    (1, 2, None)
    """
