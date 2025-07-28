"""Provides an interface like pexpect.spawn interface using subprocess.Popen"""

import subprocess
from _typeshed import StrOrBytesPath
from collections.abc import Callable
from os import _Environ
from typing import AnyStr

from .spawnbase import SpawnBase, _Logfile

class PopenSpawn(SpawnBase[AnyStr]):
    proc: subprocess.Popen[AnyStr]
    closed: bool
    def __init__(
        self,
        cmd,
        timeout: float | None = 30,
        maxread: int = 2000,
        searchwindowsize: int | None = None,
        logfile: _Logfile | None = None,
        cwd: StrOrBytesPath | None = None,
        env: _Environ[str] | None = None,
        encoding: str | None = None,
        codec_errors: str = "strict",
        preexec_fn: Callable[[], None] | None = None,
    ) -> None: ...
    flag_eof: bool
    def read_nonblocking(self, size, timeout): ...  # type: ignore[override]
    def write(self, s) -> None:
        """This is similar to send() except that there is no return value."""

    def writelines(self, sequence) -> None:
        """This calls write() for each element in the sequence.

        The sequence can be any iterable object producing strings, typically a
        list of strings. This does not add line separators. There is no return
        value.
        """

    def send(self, s):
        """Send data to the subprocess' stdin.

        Returns the number of bytes written.
        """

    def sendline(self, s: str = ""):
        """Wraps send(), sending string ``s`` to child process, with os.linesep
        automatically appended. Returns number of bytes written.
        """
    terminated: bool
    def wait(self):
        """Wait for the subprocess to finish.

        Returns the exit code.
        """

    def kill(self, sig) -> None:
        """Sends a Unix signal to the subprocess.

        Use constants from the :mod:`signal` module to specify which signal.
        """

    def sendeof(self) -> None:
        """Closes the stdin pipe from the writing end."""
