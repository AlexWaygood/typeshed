import io
from _typeshed import Incomplete
from collections.abc import Generator

from pyasn1 import error as error
from pyasn1.type import univ as univ

class CachingStreamWrapper(io.IOBase):
    """Wrapper around non-seekable streams.

    Note that the implementation is tied to the decoder,
    not checking for dangerous arguments for the sake
    of performance.

    The read bytes are kept in an internal cache until
    setting _markedPosition which may reset the cache.
    """

    def __init__(self, raw) -> None: ...
    def peek(self, n): ...
    def seekable(self): ...
    def seek(self, n: int = -1, whence=0): ...
    def read(self, n: int = -1): ...
    @property
    def markedPosition(self):
        """Position where the currently processed element starts.

        This is used for back-tracking in SingleItemDecoder.__call__
        and (indefLen)ValueDecoder and should not be used for other purposes.
        The client is not supposed to ever seek before this position.
        """

    def tell(self): ...

def asSeekableStream(substrate):
    """Convert object to seekable byte-stream.

    Parameters
    ----------
    substrate: :py:class:`bytes` or :py:class:`io.IOBase` or :py:class:`univ.OctetString`

    Returns
    -------
    : :py:class:`io.IOBase`

    Raises
    ------
    : :py:class:`~pyasn1.error.PyAsn1Error`
        If the supplied substrate cannot be converted to a seekable stream.
    """

def isEndOfStream(substrate) -> Generator[Incomplete, None, None]:
    """Check whether we have reached the end of a stream.

    Although it is more effective to read and catch exceptions, this
    function

    Parameters
    ----------
    substrate: :py:class:`IOBase`
        Stream to check

    Returns
    -------
    : :py:class:`bool`
    """

def peekIntoStream(substrate, size: int = -1) -> Generator[Incomplete, None, None]:
    """Peek into stream.

    Parameters
    ----------
    substrate: :py:class:`IOBase`
        Stream to read from.

    size: :py:class:`int`
        How many bytes to peek (-1 = all available)

    Returns
    -------
    : :py:class:`bytes` or :py:class:`str`
        The return type depends on Python major version
    """

def readFromStream(substrate, size: int = -1, context=None) -> Generator[Incomplete, None, None]:
    """Read from the stream.

    Parameters
    ----------
    substrate: :py:class:`IOBase`
        Stream to read from.

    Keyword parameters
    ------------------
    size: :py:class:`int`
        How many bytes to read (-1 = all available)

    context: :py:class:`dict`
        Opaque caller context will be attached to exception objects created
        by this function.

    Yields
    ------
    : :py:class:`bytes` or :py:class:`str` or :py:class:`SubstrateUnderrunError`
        Read data or :py:class:`~pyasn1.error.SubstrateUnderrunError`
        object if no `size` bytes is readily available in the stream. The
        data type depends on Python major version

    Raises
    ------
    : :py:class:`~pyasn1.error.EndOfStreamError`
        Input stream is exhausted
    """
