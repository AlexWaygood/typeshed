from _typeshed import FileDescriptorOrPath
from collections.abc import Iterator, Mapping, MutableMapping
from typing_extensions import Self

from paramiko.pkey import PKey

class _SubDict(MutableMapping[str, PKey]):
    # Internal to HostKeys.lookup()
    def __init__(self, hostname: str, entries: list[HostKeyEntry], hostkeys: HostKeys) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __delitem__(self, key: str) -> None: ...
    def __getitem__(self, key: str) -> PKey: ...
    def __setitem__(self, key: str, val: PKey) -> None: ...
    def keys(self) -> list[str]: ...  # type: ignore[override]

class HostKeys(MutableMapping[str, _SubDict]):
    """
    Representation of an OpenSSH-style "known hosts" file.  Host keys can be
    read from one or more files, and then individual hosts can be looked up to
    verify server keys during SSH negotiation.

    A `.HostKeys` object can be treated like a dict; any dict lookup is
    equivalent to calling `lookup`.

    .. versionadded:: 1.5.3
    """

    def __init__(self, filename: FileDescriptorOrPath | None = None) -> None:
        """
        Create a new HostKeys object, optionally loading keys from an OpenSSH
        style host-key file.

        :param str filename: filename to load host keys from, or ``None``
        """

    def add(self, hostname: str, keytype: str, key: PKey) -> None:
        """
        Add a host key entry to the table.  Any existing entry for a
        ``(hostname, keytype)`` pair will be replaced.

        :param str hostname: the hostname (or IP) to add
        :param str keytype: key type (``"ssh-rsa"`` or ``"ssh-dss"``)
        :param .PKey key: the key to add
        """

    def load(self, filename: FileDescriptorOrPath) -> None:
        """
        Read a file of known SSH host keys, in the format used by OpenSSH.
        This type of file unfortunately doesn't exist on Windows, but on
        posix, it will usually be stored in
        ``os.path.expanduser("~/.ssh/known_hosts")``.

        If this method is called multiple times, the host keys are merged,
        not cleared.  So multiple calls to `load` will just call `add`,
        replacing any existing entries and adding new ones.

        :param str filename: name of the file to read host keys from

        :raises: ``IOError`` -- if there was an error reading the file
        """

    def save(self, filename: FileDescriptorOrPath) -> None:
        """
        Save host keys into a file, in the format used by OpenSSH.  The order
        of keys in the file will be preserved when possible (if these keys were
        loaded from a file originally).  The single exception is that combined
        lines will be split into individual key lines, which is arguably a bug.

        :param str filename: name of the file to write

        :raises: ``IOError`` -- if there was an error writing the file

        .. versionadded:: 1.6.1
        """

    def lookup(self, hostname: str) -> _SubDict | None:
        """
        Find a hostkey entry for a given hostname or IP.  If no entry is found,
        ``None`` is returned.  Otherwise a dictionary of keytype to key is
        returned.  The keytype will be either ``"ssh-rsa"`` or ``"ssh-dss"``.

        :param str hostname: the hostname (or IP) to lookup
        :return: dict of `str` -> `.PKey` keys associated with this host
            (or ``None``)
        """

    def check(self, hostname: str, key: PKey) -> bool:
        """
        Return True if the given key is associated with the given hostname
        in this dictionary.

        :param str hostname: hostname (or IP) of the SSH server
        :param .PKey key: the key to check
        :return:
            ``True`` if the key is associated with the hostname; else ``False``
        """

    def clear(self) -> None:
        """
        Remove all host keys from the dictionary.
        """

    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: str) -> _SubDict: ...
    def __delitem__(self, key: str) -> None: ...
    def __setitem__(self, hostname: str, entry: Mapping[str, PKey]) -> None: ...
    def keys(self) -> list[str]: ...  # type: ignore[override]
    def values(self) -> list[_SubDict]: ...  # type: ignore[override]
    @staticmethod
    def hash_host(hostname: str, salt: str | None = None) -> str:
        """
        Return a "hashed" form of the hostname, as used by OpenSSH when storing
        hashed hostnames in the known_hosts file.

        :param str hostname: the hostname to hash
        :param str salt: optional salt to use when hashing
            (must be 20 bytes long)
        :return: the hashed hostname as a `str`
        """

class InvalidHostKey(Exception):
    line: str
    exc: Exception
    def __init__(self, line: str, exc: Exception) -> None: ...

class HostKeyEntry:
    """
    Representation of a line in an OpenSSH-style "known hosts" file.
    """

    valid: bool
    hostnames: list[str]
    key: PKey
    def __init__(self, hostnames: list[str] | None = None, key: PKey | None = None) -> None: ...
    @classmethod
    def from_line(cls, line: str, lineno: int | None = None) -> Self | None:
        """
        Parses the given line of text to find the names for the host,
        the type of key, and the key data. The line is expected to be in the
        format used by the OpenSSH known_hosts file. Fields are separated by a
        single space or tab.

        Lines are expected to not have leading or trailing whitespace.
        We don't bother to check for comments or empty lines.  All of
        that should be taken care of before sending the line to us.

        :param str line: a line from an OpenSSH known_hosts file
        """

    def to_line(self) -> str | None:
        """
        Returns a string in OpenSSH known_hosts file format, or None if
        the object is not in a valid state.  A trailing newline is
        included.
        """
