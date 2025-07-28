"""
Helper functionality for interoperability with stdlib `logging`.
"""

import logging
from _typeshed import Incomplete
from collections.abc import Callable, Sequence
from contextlib import _GeneratorContextManager
from typing import Any, TypeVar, overload

from ..std import tqdm as std_tqdm

_TqdmT = TypeVar("_TqdmT", bound=std_tqdm[Any])

def logging_redirect_tqdm(
    loggers: Sequence[logging.Logger] | None = None, tqdm_class: type[std_tqdm[Any]] = ...
) -> _GeneratorContextManager[None]:
    """
    Context manager redirecting console logging to `tqdm.write()`, leaving
    other logging handlers (e.g. log files) unaffected.

    Parameters
    ----------
    loggers  : list, optional
      Which handlers to redirect (default: [logging.root]).
    tqdm_class  : optional

    Example
    -------
    ```python
    import logging
    from tqdm import trange
    from tqdm.contrib.logging import logging_redirect_tqdm

    LOG = logging.getLogger(__name__)

    if __name__ == '__main__':
        logging.basicConfig(level=logging.INFO)
        with logging_redirect_tqdm():
            for i in trange(9):
                if i == 4:
                    LOG.info("console logging redirected to `tqdm.write()`")
        # logging restored
    ```
    """

# TODO: type *args, **kwargs here more precisely
@overload
def tqdm_logging_redirect(*args, tqdm_class: Callable[..., _TqdmT], **kwargs) -> _GeneratorContextManager[_TqdmT]:
    """
    Convenience shortcut for:
    ```python
    with tqdm_class(*args, **tqdm_kwargs) as pbar:
        with logging_redirect_tqdm(loggers=loggers, tqdm_class=tqdm_class):
            yield pbar
    ```

    Parameters
    ----------
    tqdm_class  : optional, (default: tqdm.std.tqdm).
    loggers  : optional, list.
    **tqdm_kwargs  : passed to `tqdm_class`.
    """

@overload
def tqdm_logging_redirect(*args, **kwargs) -> _GeneratorContextManager[std_tqdm[Incomplete]]: ...
