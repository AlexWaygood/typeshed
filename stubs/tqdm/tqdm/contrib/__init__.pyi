"""
Thin wrappers around common functions.

Subpackages contain potentially unstable extensions.
"""

from _typeshed import Incomplete
from collections.abc import Callable, Generator

from ..utils import ObjectWrapper

__all__ = ["tenumerate", "tzip", "tmap"]

class DummyTqdmFile(ObjectWrapper):
    """Dummy file-like that will write to tqdm"""

    def __init__(self, wrapped) -> None: ...
    def write(self, x, nolock: bool = False) -> None: ...
    def __del__(self) -> None: ...

def tenumerate(iterable, start: int = 0, total=None, tqdm_class: type[Incomplete] = ..., **tqdm_kwargs):
    """
    Equivalent of `numpy.ndenumerate` or builtin `enumerate`.

    Parameters
    ----------
    tqdm_class  : [default: tqdm.auto.tqdm].
    """

def tzip(iter1, *iter2plus, **tqdm_kwargs) -> Generator[Incomplete, None, None]:
    """
    Equivalent of builtin `zip`.

    Parameters
    ----------
    tqdm_class  : [default: tqdm.auto.tqdm].
    """

def tmap(function: Callable[..., Incomplete], *sequences, **tqdm_kwargs) -> Generator[Incomplete, None, None]:
    """
    Equivalent of builtin `map`.

    Parameters
    ----------
    tqdm_class  : [default: tqdm.auto.tqdm].
    """
