"""
Attempt to generalize the "feeder" part of a `.Channel`: an object which can be
read from and closed, but is reading from a buffer fed by another thread.  The
read operations are blocking and can have a timeout set.
"""

from threading import Event
from typing import AnyStr, Generic

class PipeTimeout(OSError):
    """
    Indicates that a timeout was reached on a read from a `.BufferedPipe`.
    """

class BufferedPipe(Generic[AnyStr]):
    """
    A buffer that obeys normal read (with timeout) & close semantics for a
    file or socket, but is fed data from another thread.  This is used by
    `.Channel`.
    """

    def __init__(self) -> None: ...
    def set_event(self, event: Event) -> None:
        """
        Set an event on this buffer.  When data is ready to be read (or the
        buffer has been closed), the event will be set.  When no data is
        ready, the event will be cleared.

        :param threading.Event event: the event to set/clear
        """

    def feed(self, data: AnyStr) -> None:
        """
        Feed new data into this pipe.  This method is assumed to be called
        from a separate thread, so synchronization is done.

        :param data: the data to add, as a ``str`` or ``bytes``
        """

    def read_ready(self) -> bool:
        """
        Returns true if data is buffered and ready to be read from this
        feeder.  A ``False`` result does not mean that the feeder has closed;
        it means you may need to wait before more data arrives.

        :return:
            ``True`` if a `read` call would immediately return at least one
            byte; ``False`` otherwise.
        """

    def read(self, nbytes: int, timeout: float | None = None) -> AnyStr:
        """
        Read data from the pipe.  The return value is a string representing
        the data received.  The maximum amount of data to be received at once
        is specified by ``nbytes``.  If a string of length zero is returned,
        the pipe has been closed.

        The optional ``timeout`` argument can be a nonnegative float expressing
        seconds, or ``None`` for no timeout.  If a float is given, a
        `.PipeTimeout` will be raised if the timeout period value has elapsed
        before any data arrives.

        :param int nbytes: maximum number of bytes to read
        :param float timeout:
            maximum seconds to wait (or ``None``, the default, to wait forever)
        :return: the read data, as a ``str`` or ``bytes``

        :raises:
            `.PipeTimeout` -- if a timeout was specified and no data was ready
            before that timeout
        """

    def empty(self) -> AnyStr:
        """
        Clear out the buffer and return all data that was in it.

        :return:
            any data that was in the buffer prior to clearing it out, as a
            `str`
        """

    def close(self) -> None:
        """
        Close this pipe object.  Future calls to `read` after the buffer
        has been emptied will return immediately with an empty string.
        """

    def __len__(self) -> int:
        """
        Return the number of bytes buffered.

        :return: number (`int`) of bytes buffered
        """
