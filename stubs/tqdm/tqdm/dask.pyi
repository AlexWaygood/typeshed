from _typeshed import Incomplete
from collections.abc import Callable
from typing import ClassVar
from typing_extensions import Self

__all__ = ["TqdmCallback"]

# dask.callbacks.Callback
class _Callback:
    active: ClassVar[set[tuple[Callable[..., Incomplete] | None, ...]]]
    def __init__(
        self,
        start: Incomplete | None,
        start_state: Incomplete | None,
        pretask: Incomplete | None,
        posttask: Incomplete | None,
        finish: Incomplete | None,
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...
    def register(self) -> None: ...
    def unregister(self) -> None: ...

class TqdmCallback(_Callback):
    """Dask callback for task progress."""

    tqdm_class: type[Incomplete]
    def __init__(
        self, start: Incomplete | None = ..., pretask: Incomplete | None = ..., tqdm_class: type[Incomplete] = ..., **tqdm_kwargs
    ) -> None:
        """
        Parameters
        ----------
        tqdm_class  : optional
            `tqdm` class to use for bars [default: `tqdm.auto.tqdm`].
        tqdm_kwargs  : optional
            Any other arguments used for all bars.
        """

    def display(self) -> None:
        """Displays in the current cell in Notebooks."""
