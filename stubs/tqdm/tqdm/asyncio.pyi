"""
Asynchronous progressbar decorator for iterators.
Includes a default `range` iterator printing to `stderr`.

Usage:
>>> from tqdm.asyncio import trange, tqdm
>>> async for i in trange(10):
...     ...
"""

from _typeshed import SupportsWrite
from asyncio import Future
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Iterator, Mapping
from typing import NoReturn, TypeVar, overload
from typing_extensions import Self

from .std import tqdm as std_tqdm

__all__ = ["tqdm_asyncio", "tarange", "tqdm", "trange"]

_T = TypeVar("_T")

class tqdm_asyncio(std_tqdm[_T]):
    """
    Asynchronous-friendly version of tqdm.
    """

    iterable_awaitable: bool
    iterable_next: Callable[[], _T | Awaitable[_T]]
    iterable_iterator: Iterator[_T]

    def __aiter__(self) -> Self: ...
    async def __anext__(self) -> _T: ...
    def send(self, *args, **kwargs): ...
    @classmethod
    def as_completed(
        cls,
        fs: Iterable[Awaitable[_T]],
        *,
        loop: bool | None = None,
        timeout: float | None = None,
        total: int | None = None,
        desc: str | None = ...,
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
    ) -> Iterator[Future[_T]]:
        """
        Wrapper for `asyncio.as_completed`.
        """

    @classmethod
    async def gather(
        cls,
        *fs: Awaitable[_T],
        loop: bool | None = None,
        timeout: float | None = None,
        total: int | None = None,
        iterable: Iterable[_T] = ...,
        desc: str | None = ...,
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
    ) -> list[_T]:
        """
        Wrapper for `asyncio.gather`.
        """

    @overload
    def __init__(
        self,
        iterable: Iterable[_T] | AsyncIterator[_T],
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
    @overload
    def __init__(
        self: tqdm_asyncio[NoReturn],
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

@overload
def tarange(
    start: int,
    stop: int,
    step: int | None = ...,
    *,
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
) -> tqdm_asyncio[int]:
    """
    A shortcut for `tqdm.asyncio.tqdm(range(*args), **kwargs)`.
    """

@overload
def tarange(
    stop: int,
    *,
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
) -> tqdm_asyncio[int]: ...

tqdm = tqdm_asyncio
trange = tarange
