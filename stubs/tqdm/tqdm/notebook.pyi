"""
IPython/Jupyter Notebook progressbar decorator for iterators.
Includes a default `range` iterator printing to `stderr`.

Usage:
>>> from tqdm.notebook import trange, tqdm
>>> for i in trange(10):
...     ...
"""

from _typeshed import Incomplete, SupportsWrite
from collections.abc import Iterable, Iterator, Mapping
from typing import NoReturn, TypeVar, overload

from .std import tqdm as std_tqdm, trange as trange

__all__ = ["tqdm_notebook", "tnrange", "tqdm", "trange"]

_T = TypeVar("_T")

class tqdm_notebook(std_tqdm[_T]):
    """
    Experimental IPython/Jupyter Notebook widget using tqdm!
    """

    @staticmethod
    def status_printer(
        _: SupportsWrite[str] | None, total: float | None = None, desc: str | None = None, ncols: int | None = None
    ):
        """
        Manage the printing of an IPython/Jupyter Notebook progress bar widget.
        """
    displayed: bool
    def display(
        self,
        msg: str | None = None,
        pos: int | None = None,
        close: bool = False,
        bar_style: str | None = None,
        check_delay: bool = True,
    ) -> None: ...
    @property
    def colour(self): ...
    @colour.setter
    def colour(self, bar_color: str) -> None: ...
    disp: Incomplete
    ncols: Incomplete
    container: Incomplete
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
        disable: bool = ...,
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
        display: bool = ...,
        **kwargs,
    ) -> None:
        """
        Supports the usual `tqdm.tqdm` parameters as well as those listed below.

        Parameters
        ----------
        display  : Whether to call `display(self.container)` immediately
            [default: True].
        """

    @overload
    def __init__(
        self: tqdm_notebook[NoReturn],
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
        disable: bool = ...,
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
        display: bool = ...,
        **kwargs,
    ) -> None: ...
    def __iter__(self) -> Iterator[_T]: ...
    def update(self, n: int = 1): ...  # type: ignore[override]
    def close(self) -> None: ...
    def clear(self, *_, **__) -> None: ...
    def reset(self, total: float | None = None):
        """
        Resets to 0 iterations for repeated use.

        Consider combining with `leave=True`.

        Parameters
        ----------
        total  : int or float, optional. Total to use for the new bar.
        """

tqdm = tqdm_notebook
tnrange = trange
