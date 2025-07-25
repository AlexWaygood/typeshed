from collections.abc import Callable
from typing import Any, TypeVar

_C = TypeVar("_C", bound=Callable[..., Any])

# Technically, the first argument of `_C` must be `Store`,
# but for now we leave it simple:
def initialised(func: _C) -> _C:
    """Check that the store is initialised before running.

    Used as a decorator in methods for :class:`passpy.store.Store`.

    :param func: A method of :class:`passpy.store.Store`.
    :type store: function

    :rtype: function
    :returns: The method if the store is initialised.

    :raises passpy.exceptions.StoreNotInitialisedError: if the store
        is not initialised.

    """

def trap(path_index: str | int) -> Callable[[_C], _C]:
    """Prevent accessing files and directories outside the password store.

    `path_index` is necessary as the functions that need to be trapped
    have different argument lists.  This way we can indicate which
    argument contains the paths that are to be checked.

    :param path_index: The index for the path variable in either
        `args` or `kwargs`.
    :type path_index: int or str

    :rtype: func
    :returns: The trapped function.

    """

def gen_password(length: int, symbols: bool = True) -> str:
    """Generates a random string.

    Uses :class:`random.SystemRandom` if available and
    :class:`random.Random` otherwise.

    :param int length: The length of the random string.

    :param bool symbols: (optional) If ``True``
        :const:`string.punctuation` will also be used to generate the
        output.

    :rtype: str
    :returns: A random string of length `length`.

    """

def copy_move(
    src: str, dst: str, force: bool = False, move: bool = False, interactive: bool = False, verbose: bool = False
) -> str | None:
    """Copies/moves a file or directory recursively.

    This function is partially based on the `cp` function from the
    `pycoreutils`_ package written by Hans van Leeuwen and licensed
    under the MIT license.

    .. _pycoreutils: https://pypi.python.org/pypi/pycoreutils/

    :param str src: The file or directory to be copied.

    :param str dst: The file or directory to be copied to.

    :param bool force: If ``True`` existing files at the destination
        will be silently overwritten.

    :param bool interactive: If ``True`` the user will be prompted for
        every file to be overwritten.  Has no effect if `force` is
        also ``True``.

    :param bool verbose: If ``True`` print the old and new filename
        for every copied/moved file.

    :raises FileNotFoundError: if there exists no key or directory for
        `src`.

    :raises FileExistsError: if a key at `dst` already exists and
        `force` is set to ``False``.

    """
