from os import stat_result
from typing_extensions import Self

class SFTPAttributes:
    """
    Representation of the attributes of a file (or proxied file) for SFTP in
    client or server mode.  It attempts to mirror the object returned by
    `os.stat` as closely as possible, so it may have the following fields,
    with the same meanings as those returned by an `os.stat` object:

        - ``st_size``
        - ``st_uid``
        - ``st_gid``
        - ``st_mode``
        - ``st_atime``
        - ``st_mtime``

    Because SFTP allows flags to have other arbitrary named attributes, these
    are stored in a dict named ``attr``.  Occasionally, the filename is also
    stored, in ``filename``.
    """

    FLAG_SIZE: int
    FLAG_UIDGID: int
    FLAG_PERMISSIONS: int
    FLAG_AMTIME: int
    FLAG_EXTENDED: int
    st_size: int | None
    st_uid: int | None
    st_gid: int | None
    st_mode: int | None
    st_atime: int | None
    st_mtime: int | None
    filename: str  # only when from_stat() is used
    longname: str  # only when from_stat() is used
    attr: dict[str, str]
    def __init__(self) -> None:
        """
        Create a new (empty) SFTPAttributes object.  All fields will be empty.
        """

    @classmethod
    def from_stat(cls, obj: stat_result, filename: str | None = None) -> Self:
        """
        Create an `.SFTPAttributes` object from an existing ``stat`` object (an
        object returned by `os.stat`).

        :param object obj: an object returned by `os.stat` (or equivalent).
        :param str filename: the filename associated with this file.
        :return: new `.SFTPAttributes` object with the same attribute fields.
        """

    def asbytes(self) -> bytes: ...
