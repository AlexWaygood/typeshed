"""
`rich.progress` decorator for iterators.

Usage:
>>> from tqdm.rich import trange, tqdm
>>> for i in trange(10):
...     ...
"""

from _typeshed import Incomplete, SupportsWrite
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from typing import NoReturn, TypeVar, overload

from .std import tqdm as std_tqdm

__all__ = ["tqdm_rich", "trrange", "tqdm", "trange"]

_T = TypeVar("_T")

# Actually rich.progress.ProgressColumn
class _ProgressColumn(ABC):
    max_refresh: float | None
    def __init__(self, table_column: Incomplete | None = ...) -> None: ...
    def get_table_column(self): ...
    def __call__(self, task): ...
    @abstractmethod
    def render(self, task): ...

class FractionColumn(_ProgressColumn):
    """Renders completed/total, e.g. '0.5/2.3 G'."""

    unit_scale: bool
    unit_divisor: int

    def __init__(self, unit_scale: bool = ..., unit_divisor: int = ...) -> None: ...
    def render(self, task):
        """Calculate common unit for completed and total."""

class RateColumn(_ProgressColumn):
    """Renders human readable transfer speed."""

    unit: str
    unit_scale: bool
    unit_divisor: int

    def __init__(self, unit: str = ..., unit_scale: bool = ..., unit_divisor: int = ...) -> None: ...
    def render(self, task):
        """Show data transfer speed."""

class tqdm_rich(std_tqdm[_T]):
    """Experimental rich.progress GUI version of tqdm!"""

    def close(self) -> None: ...
    def clear(self, *_, **__) -> None: ...
    def display(self, *_, **__) -> None: ...
    def reset(self, total: Incomplete | None = ...) -> None:
        """
        Resets to 0 iterations for repeated use.

        Parameters
        ----------
        total  : int or float, optional. Total to use for the new bar.
        """

    @overload
    def __init__(
        self,
        iterable: Iterable[_T],
        desc: str | None = ...,
        total: float | None = ...,
        leave: bool | None = ...,
        file: SupportsWrite[str] | None = ...,
        ncols: int | None = ...,
        mininterval: float = ...,
        maxinterval: float = ...,
        miniters: float | None = ...,
        ascii: bool | str | None = ...,
        disable: bool | None = ...,
        unit: str = ...,
        unit_scale: bool | float = ...,
        dynamic_ncols: bool = ...,
        smoothing: float = ...,
        bar_format: str | None = ...,
        initial: float = ...,
        position: int | None = ...,
        postfix: Mapping[str, object] | str | None = ...,
        unit_divisor: float = ...,
        write_bytes: bool | None = ...,
        lock_args: tuple[bool | None, float | None] | tuple[bool | None] | None = ...,
        nrows: int | None = ...,
        colour: str | None = ...,
        delay: float | None = ...,
        gui: bool = ...,
        **kwargs,
    ) -> None:
        """
        This class accepts the following parameters *in addition* to
        the parameters accepted by `tqdm`.

        Parameters
        ----------
        progress  : tuple, optional
            arguments for `rich.progress.Progress()`.
        options  : dict, optional
            keyword arguments for `rich.progress.Progress()`.
        """

    @overload
    def __init__(
        self: tqdm_rich[NoReturn],
        iterable: None = None,
        desc: str | None = ...,
        total: float | None = ...,
        leave: bool | None = ...,
        file: SupportsWrite[str] | None = ...,
        ncols: int | None = ...,
        mininterval: float = ...,
        maxinterval: float = ...,
        miniters: float | None = ...,
        ascii: bool | str | None = ...,
        disable: bool | None = ...,
        unit: str = ...,
        unit_scale: bool | float = ...,
        dynamic_ncols: bool = ...,
        smoothing: float = ...,
        bar_format: str | None = ...,
        initial: float = ...,
        position: int | None = ...,
        postfix: Mapping[str, object] | str | None = ...,
        unit_divisor: float = ...,
        write_bytes: bool | None = ...,
        lock_args: tuple[bool | None, float | None] | tuple[bool | None] | None = ...,
        nrows: int | None = ...,
        colour: str | None = ...,
        delay: float | None = ...,
        gui: bool = ...,
        **kwargs,
    ) -> None: ...

def trrange(*args, **kwargs) -> tqdm_rich[int]:
    """Shortcut for `tqdm.rich.tqdm(range(*args), **kwargs)`."""

tqdm = tqdm_rich
trange = trrange
