"""Virtually every Python programmer has used Python for wrangling
disk contents, and ``fileutils`` collects solutions to some of the
most commonly-found gaps in the standard library.
"""

from _typeshed import BytesPath, StrOrBytesPath, StrPath
from collections.abc import Callable, Generator, Iterable
from os import PathLike
from types import TracebackType
from typing import IO, Any, NoReturn, TypeVar, overload
from typing_extensions import Self

_StrPathT = TypeVar("_StrPathT", bound=StrPath)
_BytesPathT = TypeVar("_BytesPathT", bound=BytesPath)

def mkdir_p(path: StrOrBytesPath) -> None:
    """Creates a directory and any parent directories that may need to
    be created along the way, without raising errors for any existing
    directories. This function mimics the behavior of the ``mkdir -p``
    command available in Linux/BSD environments, but also works on
    Windows.
    """

def rotate_file(filename: PathLike[str], *, keep: int = 5) -> None:
    """
    If *filename.ext* exists, it will be moved to *filename.1.ext*,
    with all conflicting filenames being moved up by one, dropping any files beyond *keep*.

    After rotation, *filename* will be available for creation as a new file.

    Fails if *filename* is not a file or if *keep* is not > 0.
    """

class FilePerms:
    """The :class:`FilePerms` type is used to represent standard POSIX
    filesystem permissions:

      * Read
      * Write
      * Execute

    Across three classes of user:

      * Owning (u)ser
      * Owner's (g)roup
      * Any (o)ther user

    This class assists with computing new permissions, as well as
    working with numeric octal ``777``-style and ``rwx``-style
    permissions. Currently it only considers the bottom 9 permission
    bits; it does not support sticky bits or more advanced permission
    systems.

    Args:
        user (str): A string in the 'rwx' format, omitting characters
            for which owning user's permissions are not provided.
        group (str): A string in the 'rwx' format, omitting characters
            for which owning group permissions are not provided.
        other (str): A string in the 'rwx' format, omitting characters
            for which owning other/world permissions are not provided.

    There are many ways to use :class:`FilePerms`:

    >>> FilePerms(user='rwx', group='xrw', other='wxr')  # note character order
    FilePerms(user='rwx', group='rwx', other='rwx')
    >>> int(FilePerms('r', 'r', ''))
    288
    >>> oct(288)[-3:]  # XXX Py3k
    '440'

    See also the :meth:`FilePerms.from_int` and
    :meth:`FilePerms.from_path` classmethods for useful alternative
    ways to construct :class:`FilePerms` objects.
    """

    user: str
    group: str
    other: str
    def __init__(self, user: str = "", group: str = "", other: str = "") -> None: ...
    @classmethod
    def from_int(cls, i: int) -> Self:
        """Create a :class:`FilePerms` object from an integer.

        >>> FilePerms.from_int(0o644)  # note the leading zero-oh for octal
        FilePerms(user='rw', group='r', other='r')
        """

    @classmethod
    def from_path(cls, path: StrOrBytesPath) -> Self:
        """Make a new :class:`FilePerms` object based on the permissions
        assigned to the file or directory at *path*.

        Args:
            path (str): Filesystem path of the target file.

        Here's an example that holds true on most systems:

        >>> import tempfile
        >>> 'r' in FilePerms.from_path(tempfile.gettempdir()).user
        True
        """

    def __int__(self) -> int: ...

def atomic_save(dest_path: str, **kwargs) -> AtomicSaver:
    """A convenient interface to the :class:`AtomicSaver` type. Example:

    >>> try:
    ...     with atomic_save("file.txt", text_mode=True) as fo:
    ...         _ = fo.write('bye')
    ...         1/0  # will error
    ...         fo.write('bye')
    ... except ZeroDivisionError:
    ...     pass  # at least our file.txt didn't get overwritten

    See the :class:`AtomicSaver` documentation for details.
    """

class AtomicSaver:
    """``AtomicSaver`` is a configurable `context manager`_ that provides
    a writable :class:`file` which will be moved into place as long as
    no exceptions are raised within the context manager's block. These
    "part files" are created in the same directory as the destination
    path to ensure atomic move operations (i.e., no cross-filesystem
    moves occur).

    Args:
        dest_path (str): The path where the completed file will be
            written.
        overwrite (bool): Whether to overwrite the destination file if
            it exists at completion time. Defaults to ``True``.
        file_perms (int): Integer representation of file permissions
            for the newly-created file. Defaults are, when the
            destination path already exists, to copy the permissions
            from the previous file, or if the file did not exist, to
            respect the user's configured `umask`_, usually resulting
            in octal 0644 or 0664.
        text_mode (bool): Whether to open the destination file in text
            mode (i.e., ``'w'`` not ``'wb'``). Defaults to ``False`` (``wb``).
        part_file (str): Name of the temporary *part_file*. Defaults
            to *dest_path* + ``.part``. Note that this argument is
            just the filename, and not the full path of the part
            file. To guarantee atomic saves, part files are always
            created in the same directory as the destination path.
        overwrite_part (bool): Whether to overwrite the *part_file*,
            should it exist at setup time. Defaults to ``False``,
            which results in an :exc:`OSError` being raised on
            pre-existing part files. Be careful of setting this to
            ``True`` in situations when multiple threads or processes
            could be writing to the same part file.
        rm_part_on_exc (bool): Remove *part_file* on exception cases.
            Defaults to ``True``, but ``False`` can be useful for
            recovery in some cases. Note that resumption is not
            automatic and by default an :exc:`OSError` is raised if
            the *part_file* exists.

    Practically, the AtomicSaver serves a few purposes:

      * Avoiding overwriting an existing, valid file with a partially
        written one.
      * Providing a reasonable guarantee that a part file only has one
        writer at a time.
      * Optional recovery of partial data in failure cases.

    .. _context manager: https://docs.python.org/2/reference/compound_stmts.html#with
    .. _umask: https://en.wikipedia.org/wiki/Umask

    """

    dest_path: str
    overwrite: bool
    file_perms: int | None
    overwrite_part: bool
    part_filename: str | None
    rm_part_on_exc: bool
    text_mode: bool
    buffering: int
    dest_dir: str
    part_path: str
    mode: str
    open_flags: int
    part_file: str | None
    def __init__(self, dest_path: str, **kwargs) -> None: ...
    def setup(self) -> None:
        """Called on context manager entry (the :keyword:`with` statement),
        the ``setup()`` method creates the temporary file in the same
        directory as the destination file.

        ``setup()`` tests for a writable directory with rename permissions
        early, as the part file may not be written to immediately (not
        using :func:`os.access` because of the potential issues of
        effective vs. real privileges).

        If the caller is not using the :class:`AtomicSaver` as a
        context manager, this method should be called explicitly
        before writing.
        """

    def __enter__(self) -> IO[Any] | None: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...

def iter_find_files(
    directory: str,
    patterns: str | Iterable[str],
    ignored: str | Iterable[str] | None = None,
    include_dirs: bool = False,
    max_depth: int | None = None,
) -> Generator[str, None, None]:
    """Returns a generator that yields file paths under a *directory*,
    matching *patterns* using `glob`_ syntax (e.g., ``*.txt``). Also
    supports *ignored* patterns.

    Args:
        directory (str): Path that serves as the root of the
            search. Yielded paths will include this as a prefix.
        patterns (str or list): A single pattern or list of
            glob-formatted patterns to find under *directory*.
        ignored (str or list): A single pattern or list of
            glob-formatted patterns to ignore.
        include_dirs (bool): Whether to include directories that match
           patterns, as well. Defaults to ``False``.
        max_depth (int): traverse up to this level of subdirectory.
           I.e., 0 for the specified *directory* only, 1 for *directory*
           and one level of subdirectory.

    For example, finding Python files in the current directory:

    >>> _CUR_DIR = os.path.dirname(os.path.abspath(__file__))
    >>> filenames = sorted(iter_find_files(_CUR_DIR, '*.py'))
    >>> os.path.basename(filenames[-1])
    'urlutils.py'

    Or, Python files while ignoring emacs lockfiles:

    >>> filenames = iter_find_files(_CUR_DIR, '*.py', ignored='.#*')

    .. _glob: https://en.wikipedia.org/wiki/Glob_%28programming%29

    """

@overload
def copy_tree(
    src: _StrPathT, dst: _StrPathT, symlinks: bool = False, ignore: Callable[[_StrPathT, list[str]], Iterable[str]] | None = None
) -> None:
    """The ``copy_tree`` function is an exact copy of the built-in
    :func:`shutil.copytree`, with one key difference: it will not
    raise an exception if part of the tree already exists. It achieves
    this by using :func:`mkdir_p`.

    As of Python 3.8, you may pass :func:`shutil.copytree` the
    `dirs_exist_ok=True` flag to achieve the same effect.

    Args:
        src (str): Path of the source directory to copy.
        dst (str): Destination path. Existing directories accepted.
        symlinks (bool): If ``True``, copy symlinks rather than their
            contents.
        ignore (callable): A callable that takes a path and directory
            listing, returning the files within the listing to be ignored.

    For more details, check out :func:`shutil.copytree` and
    :func:`shutil.copy2`.

    """

@overload
def copy_tree(
    src: _BytesPathT,
    dst: _BytesPathT,
    symlinks: bool = False,
    ignore: Callable[[_BytesPathT, list[bytes]], Iterable[bytes]] | None = None,
) -> None: ...

copytree = copy_tree

class DummyFile:
    name: StrOrBytesPath
    mode: str
    closed: bool
    errors: None
    isatty: bool
    encoding: None
    newlines: None
    softspace: int
    def __init__(self, path: StrOrBytesPath, mode: str = "r", buffering: int | None = None) -> None: ...
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def next(self) -> NoReturn: ...
    def read(self, size: int = 0) -> str: ...
    def readline(self, size: int = 0) -> str: ...
    def readlines(self, size: int = 0) -> list[str]: ...
    def seek(self) -> None: ...
    def tell(self) -> int: ...
    def truncate(self) -> None: ...
    def write(self, string: str) -> None: ...
    def writelines(self, list_of_strings: list[str]) -> None: ...
    def __next__(self) -> NoReturn: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

__all__ = ["mkdir_p", "atomic_save", "AtomicSaver", "FilePerms", "iter_find_files", "copytree"]
