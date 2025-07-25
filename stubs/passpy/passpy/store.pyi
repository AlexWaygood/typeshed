from _typeshed import StrPath
from collections.abc import Iterator
from re import Match

class Store:
    """Python implementation of ZX2C4's password store."""

    def __init__(
        self,
        gpg_bin: str = "gpg2",
        git_bin: str = "git",
        store_dir: str = "~/.password-store",
        use_agent: bool = True,
        interactive: bool = False,
        verbose: bool = False,
    ) -> None:
        """Creates a new Store object.

        :param str gpg_bin: (optional) The path to the gpg
            binary.

        :param str git_bin: (optional) The path to the git binary.
            CURRENTLY DOES NOTHING You will need to set the
            environmental variable GIT_PYTHON_GIT_EXECUTABLE to your
            path to git binary if your git binary not in your PATH
            already.

        :param str store_dir: (optional) The path to the password store.  Will
            use the value of the PASSWORD_STORE_DIR environment variable by
            default, or `~/.password-store`, if not set.

        :param bool use_agent: (optional) Set to ``True`` if you are
            using a gpg agent.

        :param bool interactive: (optional) If ``True`` the user will
            be prompted before overwriting/deleting files.

        :param bool verbose: (optional) If ``True`` additional
            information will be printed to the standard out.

        """

    def __iter__(self) -> Iterator[str]: ...
    def is_init(self) -> bool: ...
    def init_store(self, gpg_ids: None | str | list[str], path: StrPath | None = None) -> None:
        """Initialise the password store or a subdirectory with the gpg ids.

        :param list gpg_ids: The list of gpg ids to encrypt the
            password store with.  If the list is empty, the current
            gpg id will be removed from the directory in path or root,
            if path is None.

        :param str path: (optional) If given, the gpg ids will only be
            set for the given directory.  The path is relative to
            :attr:`passpy.store.Store.store_dir`.

        :raises ValueError: if the there is a problem with `path`.

        :raises FileExistsError: if
            :attr:`passpy.store.Store.store_dir` already exists and is
            a file.

        :raises FileNotFoundError: if the current gpg id should be
            deleted, but none exists.

        :raises OSError: if the directories in path do not exist and
            can't be created.

        """

    def init_git(self) -> None:
        """Initialise git for the password store.

        Silently fails if :attr:`passpy.store.Store.repo` is not
        ``None``.

        """

    def git(self, method: str, *args: object, **kwargs: object) -> None: ...
    def get_key(self, path: StrPath | None) -> str | None:
        """Reads the data of the key at path.

        :param str path: The path to the key (without '.gpg' ending)
            relative to :attr:`passpy.store.Store.store_dir`.

        :rtype: str
        :returns: The key data as a string or ``None``, if the key
            does not exist.

        :raises FileNotFoundError: if `path` is not a file.

        """

    def set_key(self, path: StrPath | None, key_data: str, force: bool = False) -> None:
        """Add a key to the store or update an existing one.

        :param str path: The key to write.

        :param str key_data: The data of the key.

        :param bool foce: (optional) If ``True`` path will be
            overwritten if it exists.

        :raises FileExistsError: if a key already exists for path and
            overwrite is ``False``.

        """

    def remove_path(self, path: StrPath, recursive: bool = False, force: bool = False) -> None:
        """Removes the given key or directory from the store.

        :param str path: The key or directory to remove.  Use '' to
            delete the whole store.

        :param bool recursive: (optional) Set to ``True`` if nonempty
            directories should be removed.

        :param bool force: (optional) If ``True`` the user will never
            be prompted for deleting a file or directory, even if
            :attr:`passpy.store.Store.interactive` is set.

        """

    def gen_key(
        self, path: StrPath | None, length: int, symbols: bool = True, force: bool = False, inplace: bool = False
    ) -> str | None:
        """Generate a new password for a key.

        :param str path: The path of the key.

        :param int length: The length of the new password.

        :param bool symbols: (optional) If ``True`` non alphanumeric
            characters will also be used in the new password.

        :param bool force: (optional) If ``True`` an existing key at
            `path` will be overwritten.

        :param bool inplace: (optional) If ``True`` only the first
            line of an existing key at `path` will be overwritten with
            the new password.

        """

    def copy_path(self, old_path: StrPath, new_path: StrPath, force: bool = False) -> None:
        """Copies a key or directory within the password store.

        :param str old_path: The current path of the key or directory.

        :param str new_path: The new path of the key or directory.  If
            `new_path` ends in a trailing '/' it will always be
            treated as a directory.

        :param bool force: If ``True`` any existing key or directory at
            `new_path` will be overwritten.

        """

    def move_path(self, old_path: StrPath, new_path: StrPath, force: bool = False) -> None:
        """Moves a key or directory within the password store.

        :param str old_path: The current path of the key or directory.

        :param str new_path: The new path of the key or directory.  If
            `new_path` ends in a trailing '/' it will always be
            treated as a directory.

        :param bool force: If ``True`` any existing key or directory at
            `new_path` will be overwritten.

        """

    def list_dir(self, path: StrPath) -> tuple[list[str], list[str]]:
        """Returns all directory and key entries for the given path.

        :param str path: The directory to list relative to
            :attr:`passpy.store.Store.store_dir`

        :rtype: (list, list)
        :returns: Two lists, the first for directories, the second for
            keys.  ``None`` if `path` is not a directory.

        :raises FileNotFoundError: if `path` is not a directory in the
            password store.

        """

    def iter_dir(self, path: StrPath) -> Iterator[str]: ...
    def find(self, names: None | str | list[str]) -> list[str]:
        """Find keys by name.

        Finds any keys in the password store that contain any one
        entry in `names`.

        :param names: The name or names to find keys for.
        :type names: str or list

        :rtype: list
        :returns: A list of keys whose name contain any one entry in
            `names`.

        """

    def search(self, term: str) -> dict[str, list[tuple[str, Match[str]]]]:
        """Search through all keys.

        :param str term: The term to search for.  The term will be
            compiled as a regular expression.

        :rtype: dict
        :returns: The dictionary has an entry for each key, that
            matched the given term.  The entry for that key then
            contains a list of tuples with the line the term was found
            on and the match object.

        """
