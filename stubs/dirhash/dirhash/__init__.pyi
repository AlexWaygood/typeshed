"""dirhash - a python library (and CLI) for hashing of file system directories."""

from _typeshed import Incomplete
from collections.abc import Generator, Iterable
from os import PathLike
from typing import TypeVar
from typing_extensions import TypeAlias

_DirNode: TypeAlias = Incomplete  # scantree.DirNode
_RecursionPath: TypeAlias = Incomplete  # scantree.RecursionPath
_RP = TypeVar("_RP", bound=_RecursionPath)

__all__ = [
    "__version__",
    "algorithms_guaranteed",
    "algorithms_available",
    "dirhash",
    "dirhash_impl",
    "included_paths",
    "Filter",
    "get_match_patterns",
    "Protocol",
]

__version__: str
algorithms_guaranteed: set[str]
algorithms_available: set[str]

def dirhash(
    directory: str | PathLike[str],
    algorithm: str,
    match: Iterable[str] = ("*",),
    ignore: Iterable[str] | None = None,
    linked_dirs: bool = True,
    linked_files: bool = True,
    empty_dirs: bool = False,
    entry_properties: Iterable[str] = ("name", "data"),
    allow_cyclic_links: bool = False,
    chunk_size: int = 1048576,
    jobs: int = 1,
) -> str:
    """Computes the hash of a directory based on its structure and content.

    # Arguments
        directory: Union[str, pathlib.Path] - Path to the directory to hash.
        algorithm: str - The name of the hashing algorithm to use. See
            `dirhash.algorithms_available` for the available options.
        match: Iterable[str] - An iterable of glob/wildcard match-patterns for paths
            to include when computing the hash. Default is ["*"] which means that all
            files and directories are matched.  To e.g. only include python source
            files, use: `match=["*.py"]`. See "Path Selection and Filtering" section
            below for further details.
        ignore: Optional[Iterable[str]] - An iterable of glob/wildcard match-patterns
            for paths to ignore when computing the hash. Default `None` (no ignore
            patterns). To e.g. exclude hidden files and directories use:
            `ignore=[".*/", ".*"]`. See "Path Selection and Filtering" section below
            for further details.
        linked_dirs: bool - If `True` (default), follow symbolic links to other
            *directories* and include these and their content in the hash
            computation.
        linked_files: bool - If `True` (default), include symbolic linked files in
            the hash computation.
        empty_dirs: bool - If `True`, include empty directories when computing the
            hash. A directory is considered empty if it does not contain any files
            that *matches provided matching criteria*. Default `False`, i.e. empty
            directories are ignored (as is done in git version control).
        entry_properties: Iterable[str] - A set (i.e. order does not matter) of the
            file/directory properties to consider when computing the hash. Supported
            properties are {"name", "data", "is_link"} where at least one of
            "name" and "data" must be included. Default is ["name", "data"] which
            means that the content (actual data) as well as the path relative to the
            root `directory` of files will affect the hash value. See "Entry
            Properties Interpretation" section below for further details.
        allow_cyclic_links: bool - If `False` (default) a `SymlinkRecursionError` is
            raised on presence of cyclic symbolic links. If set to `True` the the
            dirhash value for directory causing the cyclic link is replaced with the
            hash function hexdigest of the relative path from the link to the target.
        chunk_size: int - The number of bytes to read in one go from files while
            being hashed. A too small size will slow down the processing and a larger
            size consumes more working memory. Default 2**20 byte = 1 MiB.
        jobs: int - The number of processes to use when computing the hash.
            Default `1`, which means that a single (the main) process is used. NOTE
            that using multiprocessing can significantly speed-up execution, see
            `https://github.com/andhus/dirhash-python/benchmark` for further
            details.

    # Returns
        str - The hash/checksum as a string of the hexadecimal digits (the result of
        `hexdigest` method of the hashlib._hashlib.HASH object corresponding to the
        provided `algorithm`).

    # Raises
        TypeError/ValueError: For incorrectly provided arguments.
        SymlinkRecursionError: In case the `directory` contains symbolic links that
            lead to (infinite) recursion and `allow_cyclic_links=False` (default).

    # Path Selection and Filtering
        Provided glob/wildcard (".gitignore style") match-patterns determine what
        paths within the `directory` to include when computing the hash value. Paths
        *relative to the root `directory`* (i.e. excluding the name of the root
        directory itself) are matched against the patterns.
            The `match` argument represent what should be *included* - as opposed
        to the `ignore` argument for which matches are *excluded*. Using `ignore` is
        just short for adding the same patterns to the `match` argument with the
        prefix "!", i.e. the calls bellow are equivalent:
            `dirhash(..., match=["*", "!<pattern>"])`
            `dirhash(..., ignore=["<pattern>"])`
        To validate which paths are included, call `dirhash.included_paths` with
        the same values for the arguments: `match`, `ignore`, `linked_dirs`,
        `linked_files` and `empty_dirs` to get a list of all paths that will be
        included when computing the hash by this function.

    # Entry Properties Interpretation
        - ["name", "data"] (Default) - The name as well as data is included. Due to
            the recursive nature of the dirhash computation, "name" implies that the
            path relative to the root `directory` of each file/directory affects the
            computed hash value.
        - ["data"] - Compute the hash only based on the data of files -
            *not* their names or the names of their parent directories. NOTE that
            the tree structure in which files are organized under the `directory`
            root still influences the computed hash. As longs as all files have
            the same content and are organised the same way in relation to all
            other files in the Directed Acyclic Graph representing the file-tree,
            the hash will remain the same (but the "name of nodes" does not
            matter). This option can e.g. be used to verify that that data is
            unchanged after renaming files (change extensions etc.).
        - ["name"] - Compute the hash only based on the name and location of
            files in the file tree under the `directory` root. This option can
            e.g. be used to check if any files have been added/moved/removed,
            ignoring the content of each file.
        - "is_link" - if this options is added to any of the cases above the
            hash value is also affected by whether a file or directory is a
            symbolic link or not. NOTE: with this property added, the hash
            will be different than without it even if there are no symbolic links
            in the directory.

    # References
        See https://github.com/andhus/dirhash/README.md for a formal
        description of how the returned hash value is computed.
    """

def dirhash_impl(
    directory: str | PathLike[str],
    algorithm: str,
    filter_: Filter | None = None,
    protocol: Protocol | None = None,
    chunk_size: int = 1048576,
    jobs: int = 1,
) -> str:
    """Computes the hash of a directory based on its structure and content.

    In contrast to `dirhash.dirhash`, this function accepts custom implementations of
    the `dirhash.Filter` and `dirhash.Protocol` classes.

    # Arguments
        directory: Union[str, pathlib.Path] - Path to the directory to hash.
        algorithm: str - The name of the hashing algorithm to use. See
            `dirhash.algorithms_available` for the available options.
            It is also possible to provide a callable object that returns an instance
            implementing the `hashlib._hashlib.HASH` interface.
        filter_: dirhash.Filter - Determines what files and directories to include
            when computing the hash. See docs of `dirhash.Filter` for further
            details.
        protocol: dirhash.Protocol - Determines (mainly) what properties of files and
            directories to consider when computing the hash value.
        chunk_size: int - The number of bytes to read in one go from files while
            being hashed. A too small size will slow down the processing and a larger
            size consumes more working memory. Default 2**20 byte = 1 MiB.
        jobs: int - The number of processes to use when computing the hash.
            Default `1`, which means that a single (the main) process is used. NOTE
            that using multiprocessing can significantly speed-up execution, see
            `https://github.com/andhus/dirhash/tree/master/benchmark` for further
            details.

    # Returns
        str - The hash/checksum as a string of the hexadecimal digits (the result of
        `hexdigest` method of the hashlib._hashlib.HASH object corresponding to the
        provided `algorithm`).

    # Raises
        TypeError/ValueError: For incorrectly provided arguments.
        SymlinkRecursionError: In case the `directory` contains symbolic links that
            lead to (infinite) recursion and the protocol option `allow_cyclic_links`
            is `False`.

    # References
        See https://github.com/andhus/dirhash/README.md for a formal
        description of how the returned hash value is computed.
    """

def included_paths(
    directory: str | PathLike[str],
    match: Iterable[str] = ("*",),
    ignore: Iterable[str] | None = None,
    linked_dirs: bool = True,
    linked_files: bool = True,
    empty_dirs: bool = False,
    allow_cyclic_links: bool = False,
) -> list[str]:
    """Inspect what paths are included for the corresponding arguments to the
    `dirhash.dirhash` function.

    # Arguments:
        This function accepts the following subset of the function `dirhash.dirhash`
        arguments: `directory`, `match`, `ignore`, `linked_dirs`, `linked_files`,
        `empty_dirs` and `allow_cyclic_links`, *with the same interpretation*. See
        docs of `dirhash.dirhash` for further details.

    # Returns
        List[str] - A sorted list of the paths that would be included when computing
        the hash of the `directory` using `dirhash.dirhash` and the same arguments.
    """

class Filter:
    """Specification of what files and directories to include for the `dirhash`
    computation.

    # Arguments
        match: Iterable[str] - An iterable of glob/wildcard (".gitignore style")
            match patterns for selection of which files and directories to include.
            Paths *relative to the root `directory`* (i.e. excluding the name of the
            root directory itself) are matched against the provided patterns. For
            example, to include all files, except for hidden ones use:
            `match=['*', '!.*']` Default `None` which is equivalent to `['*']`,
            i.e. everything is included.
        linked_dirs: bool - If `True` (default), follow symbolic links to other
            *directories* and include these and their content in the hash
            computation.
        linked_files: bool - If `True` (default), include symbolic linked files in
            the hash computation.
        empty_dirs: bool - If `True`, include empty directories when computing the
            hash. A directory is considered empty if it does not contain any files
            that *matches provided matching criteria*. Default `False`, i.e. empty
            directories are ignored (as is done in git version control).
    """

    linked_dirs: bool
    linked_files: bool
    empty_dirs: bool

    def __init__(
        self,
        match_patterns: Iterable[str] | None = None,
        linked_dirs: bool = True,
        linked_files: bool = True,
        empty_dirs: bool = False,
    ) -> None: ...
    @property
    def match_patterns(self) -> tuple[str, ...]: ...
    def include(self, recursion_path: _RecursionPath) -> bool: ...
    def match_file(self, filepath: str | PathLike[str]) -> bool:
        """Match file against match patterns.

        NOTE: only match patterns are considered, not the `linked_files` argument of
        this class.

        # Arguments:
            filepath (str): the path to match.

        # Returns:
            Boolean, whether the path is a match or not.
        """

    def __call__(self, paths: Iterable[_RP]) -> Generator[_RP, None, None]:
        """Filter recursion paths.

        # Arguments:
            paths ([RecursionPath]): The recursion paths to filter.

        # Returns:
            A generator of (filtered) recursion paths.
        """

def get_match_patterns(
    match: Iterable[str] | None = None,
    ignore: Iterable[str] | None = None,
    ignore_extensions: Iterable[str] | None = None,
    ignore_hidden: bool = False,
) -> list[str]:
    """Helper to compose a list of list of glob/wildcard (".gitignore style") match
    patterns based on options dedicated for a few standard use-cases.

    # Arguments
        match: Optional[List[str]] - A list of match-patterns for files to *include*.
            Default `None` which is equivalent to `['*']`, i.e. everything is
            included (unless excluded by arguments below).
        ignore: Optional[List[str]] -  A list of match-patterns for files to
            *ignore*. Default `None` (no ignore patterns).
        ignore_extensions: Optional[List[str]] -  A list of file extensions to
            ignore. Short for `ignore=['*.<my extension>', ...]` Default `None` (no
            extensions ignored).
        ignore_hidden: bool - If `True` ignore hidden files and directories. Short
            for `ignore=['.*', '.*/']` Default `False`.
    """

class Protocol:
    """Specifications of which file and directory properties to consider when
        computing the `dirhash` value.

    # Arguments
        entry_properties: Iterable[str] - A combination of the supported properties
            {"name", "data", "is_link"} where at least one of "name" and "data" is
            included. Interpretation:
            - ["name", "data"] (Default) - The name as well as data is included. Due
                to the recursive nature of the dirhash computation, "name" implies
                that the path relative to the root `directory` of each file/directory
                affects the computed hash value.
            - ["data"] - Compute the hash only based on the data of files -
                *not* their names or the names of their parent directories. NOTE that
                the tree structure in which files are organized under the `directory`
                root still influences the computed hash. As longs as all files have
                the same content and are organised the same way in relation to all
                other files in the Directed Acyclic Graph representing the file-tree,
                the hash will remain the same (but the "name of nodes" does not
                matter). This option can e.g. be used to verify that that data is
                unchanged after renaming files (change extensions etc.).
            - ["name"] - Compute the hash only based on the name and location of
                files in the file tree under the `directory` root. This option can
                e.g. be used to check if any files have been added/moved/removed,
                ignoring the content of each file.
            - "is_link" - if this options is added to any of the cases above the
                hash value is also affected by whether a file or directory is a
                symbolic link or not. NOTE: which this property added, the hash
                will be different than without it even if there are no symbolic links
                in the directory.
        allow_cyclic_links: bool - If `False` (default) a `SymlinkRecursionError` is
            raised on presence of cyclic symbolic links. If set to `True` the the
            dirhash value for directory causing the cyclic link is replaced with the
            hash function hexdigest of the relative path from the link to the target.
    """

    class EntryProperties:
        NAME: str
        DATA: str
        IS_LINK: str
        options: set[str]

    entry_properties: Iterable[str]
    allow_cyclic_links: bool
    def __init__(self, entry_properties: Iterable[str] = ("name", "data"), allow_cyclic_links: bool = False) -> None: ...
    def get_descriptor(self, dir_node: _DirNode) -> str: ...
