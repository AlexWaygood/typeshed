"""
Server-mode SFTP support.
"""

from _typeshed import FileDescriptorOrPath
from logging import Logger
from typing import Any

from paramiko.channel import Channel
from paramiko.server import ServerInterface, SubsystemHandler
from paramiko.sftp import BaseSFTP
from paramiko.sftp_attr import SFTPAttributes
from paramiko.sftp_handle import SFTPHandle
from paramiko.sftp_si import SFTPServerInterface
from paramiko.transport import Transport

class SFTPServer(BaseSFTP, SubsystemHandler):
    """
    Server-side SFTP subsystem support.  Since this is a `.SubsystemHandler`,
    it can be (and is meant to be) set as the handler for ``"sftp"`` requests.
    Use `.Transport.set_subsystem_handler` to activate this class.
    """

    logger: Logger
    ultra_debug: bool
    next_handle: int
    file_table: dict[bytes, SFTPHandle]
    folder_table: dict[bytes, SFTPHandle]
    server: SFTPServerInterface
    sock: Channel | None
    def __init__(
        self,
        channel: Channel,
        name: str,
        server: ServerInterface,
        sftp_si: type[SFTPServerInterface] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        The constructor for SFTPServer is meant to be called from within the
        `.Transport` as a subsystem handler.  ``server`` and any additional
        parameters or keyword parameters are passed from the original call to
        `.Transport.set_subsystem_handler`.

        :param .Channel channel: channel passed from the `.Transport`.
        :param str name: name of the requested subsystem.
        :param .ServerInterface server:
            the server object associated with this channel and subsystem
        :param sftp_si:
            a subclass of `.SFTPServerInterface` to use for handling individual
            requests.
        """

    def start_subsystem(self, name: str, transport: Transport, channel: Channel) -> None: ...
    def finish_subsystem(self) -> None: ...
    @staticmethod
    def convert_errno(e: int) -> int:
        """
        Convert an errno value (as from an ``OSError`` or ``IOError``) into a
        standard SFTP result code.  This is a convenience function for trapping
        exceptions in server code and returning an appropriate result.

        :param int e: an errno code, as from ``OSError.errno``.
        :return: an `int` SFTP error code like ``SFTP_NO_SUCH_FILE``.
        """

    @staticmethod
    def set_file_attr(filename: FileDescriptorOrPath, attr: SFTPAttributes) -> None:
        """
        Change a file's attributes on the local filesystem.  The contents of
        ``attr`` are used to change the permissions, owner, group ownership,
        and/or modification & access time of the file, depending on which
        attributes are present in ``attr``.

        This is meant to be a handy helper function for translating SFTP file
        requests into local file operations.

        :param str filename:
            name of the file to alter (should usually be an absolute path).
        :param .SFTPAttributes attr: attributes to change.
        """
