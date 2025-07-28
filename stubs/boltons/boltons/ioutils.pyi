"""
Module ``ioutils`` implements a number of helper classes and functions which
are useful when dealing with input, output, and bytestreams in a variety of
ways.
"""

import abc
from _typeshed import Incomplete
from abc import abstractmethod

READ_CHUNK_SIZE: int
EINVAL: Incomplete

class SpooledIOBase(metaclass=abc.ABCMeta):
    """
    A base class shared by the SpooledBytesIO and SpooledStringIO classes.

    The SpooledTemporaryFile class is missing several attributes and methods
    present in the StringIO implementation. This brings the api as close to
    parity as possible so that classes derived from SpooledIOBase can be used
    as near drop-in replacements to save memory.
    """

    __metaclass__: Incomplete
    def __init__(self, max_size: int = 5000000, dir=None) -> None: ...
    @abstractmethod
    def read(self, n: int = -1):
        """Read n characters from the buffer"""

    @abstractmethod
    def write(self, s):
        """Write into the buffer"""

    @abstractmethod
    def seek(self, pos, mode: int = 0):
        """Seek to a specific point in a file"""

    @abstractmethod
    def readline(self, length=None):
        """Returns the next available line"""

    @abstractmethod
    def readlines(self, sizehint: int = 0):
        """Returns a list of all lines from the current position forward"""

    def writelines(self, lines) -> None:
        """
        Write lines to the file from an interable.

        NOTE: writelines() does NOT add line separators.
        """

    @abstractmethod
    def rollover(self):
        """Roll file-like-object over into a real temporary file"""

    @abstractmethod
    def tell(self):
        """Return the current position"""

    @property
    @abc.abstractmethod
    def buffer(self):
        """Should return a flo instance"""

    @property
    @abc.abstractmethod
    def len(self):
        """Returns the length of the data"""
    softspace: Incomplete
    def close(self): ...
    def flush(self): ...
    def isatty(self): ...
    def next(self): ...
    @property
    def closed(self): ...
    @property
    def pos(self): ...
    @property
    def buf(self): ...
    def fileno(self): ...
    def truncate(self, size=None):
        """
        Truncate the contents of the buffer.

        Custom version of truncate that takes either no arguments (like the
        real SpooledTemporaryFile) or a single argument that truncates the
        value to a certain index location.
        """

    def getvalue(self):
        """Return the entire files contents."""

    def seekable(self): ...
    def readable(self): ...
    def writable(self): ...
    __next__: Incomplete
    def __len__(self): ...
    def __iter__(self): ...
    def __enter__(self): ...
    def __exit__(self, *args) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __bool__(self): ...
    def __del__(self) -> None:
        """Can fail when called at program exit so suppress traceback."""
    __nonzero__: Incomplete

class SpooledBytesIO(SpooledIOBase):
    """
    SpooledBytesIO is a spooled file-like-object that only accepts bytes. On
    Python 2.x this means the 'str' type; on Python 3.x this means the 'bytes'
    type. Bytes are written in and retrieved exactly as given, but it will
    raise TypeErrors if something other than bytes are written.

    Example::

        >>> from boltons import ioutils
        >>> with ioutils.SpooledBytesIO() as f:
        ...     f.write(b"Happy IO")
        ...     _ = f.seek(0)
        ...     isinstance(f.getvalue(), bytes)
        True
    """

    def read(self, n: int = -1): ...
    def write(self, s) -> None: ...
    def seek(self, pos, mode: int = 0): ...
    def readline(self, length=None): ...
    def readlines(self, sizehint: int = 0): ...
    def rollover(self) -> None:
        """Roll the StringIO over to a TempFile"""

    @property
    def buffer(self): ...
    @property
    def len(self):
        """Determine the length of the file"""

    def tell(self): ...

class SpooledStringIO(SpooledIOBase):
    """
    SpooledStringIO is a spooled file-like-object that only accepts unicode
    values. On Python 2.x this means the 'unicode' type and on Python 3.x this
    means the 'str' type. Values are accepted as unicode and then coerced into
    utf-8 encoded bytes for storage. On retrieval, the values are returned as
    unicode.

    Example::

        >>> from boltons import ioutils
        >>> with ioutils.SpooledStringIO() as f:
        ...     f.write(u"— Hey, an emdash!")
        ...     _ = f.seek(0)
        ...     isinstance(f.read(), str)
        True

    """

    def __init__(self, *args, **kwargs) -> None: ...
    def read(self, n: int = -1): ...
    def write(self, s) -> None: ...
    def seek(self, pos, mode: int = 0):
        """Traverse from offset to the specified codepoint"""

    def readline(self, length=None): ...
    def readlines(self, sizehint: int = 0): ...
    @property
    def buffer(self): ...
    def rollover(self) -> None:
        """Roll the buffer over to a TempFile"""

    def tell(self):
        """Return the codepoint position"""

    @property
    def len(self):
        """Determine the number of codepoints in the file"""

def is_text_fileobj(fileobj) -> bool: ...

class MultiFileReader:
    """Takes a list of open files or file-like objects and provides an
    interface to read from them all contiguously. Like
    :func:`itertools.chain()`, but for reading files.

       >>> mfr = MultiFileReader(BytesIO(b'ab'), BytesIO(b'cd'), BytesIO(b'e'))
       >>> mfr.read(3).decode('ascii')
       u'abc'
       >>> mfr.read(3).decode('ascii')
       u'de'

    The constructor takes as many fileobjs as you hand it, and will
    raise a TypeError on non-file-like objects. A ValueError is raised
    when file-like objects are a mix of bytes- and text-handling
    objects (for instance, BytesIO and StringIO).
    """

    def __init__(self, *fileobjs) -> None: ...
    def read(self, amt=None):
        """Read up to the specified *amt*, seamlessly bridging across
        files. Returns the appropriate type of string (bytes or text)
        for the input, and returns an empty string when the files are
        exhausted.
        """

    def seek(self, offset, whence=0) -> None:
        """Enables setting position of the file cursor to a given
        *offset*. Currently only supports ``offset=0``.
        """
