"""Useful utilities for working with the `mbox`_-formatted
mailboxes. Credit to Mark Williams for these.

.. _mbox: https://en.wikipedia.org/wiki/Mbox
"""

import mailbox
from _typeshed import StrPath
from collections.abc import Callable
from typing import IO, Any

DEFAULT_MAXMEM: int

class mbox_readonlydir(mailbox.mbox):
    """A subclass of :class:`mailbox.mbox` suitable for use with mboxs
    insides a read-only mail directory, e.g., ``/var/mail``. Otherwise
    the API is exactly the same as the built-in mbox.

    Deletes messages via truncation, in the manner of `Heirloom mailx`_.

    Args:
        path (str): Path to the mbox file.
        factory (type): Message type (defaults to :class:`rfc822.Message`)
        create (bool): Create mailbox if it does not exist. (defaults
                       to ``True``)
        maxmem (int): Specifies, in bytes, the largest sized mailbox
                      to attempt to copy into memory. Larger mailboxes
                      will be copied incrementally which is more
                      hazardous. (defaults to 4MB)

    .. note::

       Because this truncates and rewrites parts of the mbox file,
       this class can corrupt your mailbox.  Only use this if you know
       the built-in :class:`mailbox.mbox` does not work for your use
       case.

    .. _Heirloom mailx: http://heirloom.sourceforge.net/mailx.html
    """

    maxmem: int
    def __init__(
        self,
        path: StrPath,
        factory: Callable[[IO[Any]], mailbox.mboxMessage] | None = None,
        create: bool = True,
        maxmem: int = 1048576,
    ) -> None: ...
    def flush(self) -> None:
        """Write any pending changes to disk. This is called on mailbox
        close and is usually not called explicitly.

        .. note::

           This deletes messages via truncation. Interruptions may
           corrupt your mailbox.
        """
