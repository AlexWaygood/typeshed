from collections.abc import Callable
from typing import TypeVar, overload
from typing_extensions import TypeAlias

_AnyCallable: TypeAlias = Callable[..., object]
_Func = TypeVar("_Func", bound=_AnyCallable)

# We (ab)use this decorator to also copy the signature of the source function (overload 1)
# The advantages are:
# - avoid copying all parameters and types manually while conserving type safety
# - signature properly handeled in IDEs (at least with Pylance)
# - docstring from the original function properly displayed (at least with Pylance)
# Using the other overloads returns the signature of the decorated function instead
@overload
def doc(func: _Func, /, **params: object) -> Callable[[_AnyCallable], _Func]:
    """Append docstrings to a callable.

    A decorator take docstring templates, concatenate them and perform string
    substitution on it.
    This decorator will add a variable "_docstring_components" to the wrapped
    callable to keep track the original docstring template for potential usage.
    If it should be consider as a template, it will be saved as a string.
    Otherwise, it will be saved as callable, and later user __doc__ and dedent
    to get docstring.

    Parameters
    ----------
    *docstrings : str or callable
        The string / docstring / docstring template to be appended in order
        after default docstring under callable.
    **params
        The string which would be used to format docstring template.
    """

@overload
def doc(docstring: str, /, *docstrings: str | _AnyCallable, **params: object) -> Callable[[_Func], _Func]: ...
@overload
def doc(
    docstring1: str | _AnyCallable, docstring2: str | _AnyCallable, /, *docstrings: str | _AnyCallable, **params: object
) -> Callable[[_Func], _Func]: ...
