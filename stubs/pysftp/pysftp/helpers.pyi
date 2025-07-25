"""functions and classes that support the Connection object"""

from collections.abc import Callable, Iterator
from contextlib import AbstractContextManager
from typing_extensions import TypeAlias

def known_hosts() -> str:
    """return a proper path to ssh's known_host file for the user"""

def st_mode_to_int(val: int) -> int:
    """SFTAttributes st_mode returns an stat type that shows more than what
    can be set.  Trim off those bits and convert to an int representation.
    if you want an object that was `chmod 711` to return a value of 711, use
    this function

    :param int val: the value of an st_mode attr returned by SFTPAttributes

    :returns int: integer representation of octal mode

    """

class WTCallbacks:
    """an object to house the callbacks, used internally"""

    def __init__(self) -> None:
        """set instance vars"""

    def file_cb(self, pathname: str) -> None:
        """called for regular files, appends pathname to .flist

        :param str pathname: file path
        """

    def dir_cb(self, pathname: str) -> None:
        """called for directories, appends pathname to .dlist

        :param str pathname: directory path
        """

    def unk_cb(self, pathname: str) -> None:
        """called for unknown file types, appends pathname to .ulist

        :param str pathname: unknown entity path
        """

    @property
    def flist(self) -> list[str]:
        """return a sorted list of files currently traversed

        :getter: returns the list
        :setter: sets the list
        :type: list
        """

    @flist.setter
    def flist(self, val: list[str]) -> None: ...
    @property
    def dlist(self) -> list[str]:
        """return a sorted list of directories currently traversed

        :getter: returns the list
        :setter: sets the list
        :type: list
        """

    @dlist.setter
    def dlist(self, val: list[str]) -> None: ...
    @property
    def ulist(self) -> list[str]:
        """return a sorted list of unknown entities currently traversed

        :getter: returns the list
        :setter: sets the list
        :type: list
        """

    @ulist.setter
    def ulist(self, val: list[str]) -> None: ...

def path_advance(thepath: str, sep: str = ...) -> Iterator[str]:
    """generator to iterate over a file path forwards

    :param str thepath: the path to navigate forwards
    :param str sep: *Default: os.sep* - the path separator to use

    :returns: (iter)able of strings

    """

def path_retreat(thepath: str, sep: str = ...) -> Iterator[str]:
    """generator to iterate over a file path in reverse

    :param str thepath: the path to retreat over
    :param str sep: *Default: os.sep* - the path separator to use

    :returns: (iter)able of strings

    """

def reparent(newparent: str, oldpath: str) -> str:
    """when copying or moving a directory structure, you need to re-parent the
    oldpath.  When using os.path.join to calculate this new path, the
    appearance of a / root path at the beginning of oldpath, supplants the
    newparent and we don't want this to happen, so we need to make the oldpath
    root appear as a child of the newparent.

    :param: str newparent: the new parent location for oldpath (target)
    :param str oldpath: the path being adopted by newparent (source)

    :returns: (str) resulting adoptive path
    """

_PathCallback: TypeAlias = Callable[[str], object]

def walktree(
    localpath: str, fcallback: _PathCallback, dcallback: _PathCallback, ucallback: _PathCallback, recurse: bool = True
) -> None:
    """on the local file system, recursively descend, depth first, the
    directory tree rooted at localpath, calling discreet callback functions
    for each regular file, directory and unknown file type.

    :param str localpath:
        root of remote directory to descend, use '.' to start at
        :attr:`.pwd`
    :param callable fcallback:
        callback function to invoke for a regular file.
        (form: ``func(str)``)
    :param callable dcallback:
        callback function to invoke for a directory. (form: ``func(str)``)
    :param callable ucallback:
        callback function to invoke for an unknown file type.
        (form: ``func(str)``)
    :param bool recurse: *Default: True* -  should it recurse

    :returns: None

    :raises: OSError, if localpath doesn't exist

    """

def cd(localpath: str | None = None) -> AbstractContextManager[None]:
    """context manager that can change to a optionally specified local
    directory and restores the old pwd on exit.

    :param str|None localpath: *Default: None* -
        local path to temporarily make the current directory
    :returns: None
    :raises: OSError, if local path doesn't exist
    """
