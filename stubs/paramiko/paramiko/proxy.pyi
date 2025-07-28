from _typeshed import ReadableBuffer
from subprocess import Popen
from typing import Any

from paramiko.util import ClosingContextManager

subprocess_import_error: ImportError | None

class ProxyCommand(ClosingContextManager):
    """
    Wraps a subprocess running ProxyCommand-driven programs.

    This class implements a the socket-like interface needed by the
    `.Transport` and `.Packetizer` classes. Using this class instead of a
    regular socket makes it possible to talk with a Popen'd command that will
    proxy traffic between the client and a server hosted in another machine.

    Instances of this class may be used as context managers.
    """

    cmd: list[str]
    process: Popen[Any]
    timeout: float | None
    def __init__(self, command_line: str) -> None:
        """
        Create a new CommandProxy instance. The instance created by this
        class can be passed as an argument to the `.Transport` class.

        :param str command_line:
            the command that should be executed and used as the proxy.
        """

    def send(self, content: ReadableBuffer) -> int:
        """
        Write the content received from the SSH client to the standard
        input of the forked command.

        :param str content: string to be sent to the forked command
        """

    def recv(self, size: int) -> bytes:
        """
        Read from the standard output of the forked program.

        :param int size: how many chars should be read

        :return: the string of bytes read, which may be shorter than requested
        """

    def close(self) -> None: ...
    @property
    def closed(self) -> bool: ...
    def settimeout(self, timeout: float) -> None: ...
