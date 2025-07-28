"""
Deprecated module to handle Exceptions across Python versions.

.. warning::
   This module is deprecated with the end of support for Python 2.7
   and will be removed in Docutils 0.21 or later.

   Replacements:
     | SafeString  -> str
     | ErrorString -> docutils.io.error_string()
     | ErrorOutput -> docutils.io.ErrorOutput

Error reporting should be safe from encoding/decoding errors.
However, implicit conversions of strings and exceptions like

>>> u'%s world: %s' % ('Hällo', Exception(u'Hällo'))

fail in some Python versions:

* In Python <= 2.6, ``unicode(<exception instance>)`` uses
  `__str__` and fails with non-ASCII chars in`unicode` arguments.
  (work around http://bugs.python.org/issue2517):

* In Python 2, unicode(<exception instance>) fails, with non-ASCII
  chars in arguments. (Use case: in some locales, the errstr
  argument of IOError contains non-ASCII chars.)

* In Python 2, str(<exception instance>) fails, with non-ASCII chars
  in `unicode` arguments.

The `SafeString`, `ErrorString` and `ErrorOutput` classes handle
common exceptions.
"""

from io import TextIOWrapper
from typing import TextIO
from typing_extensions import TypeAlias, deprecated

unicode = str

_DataType: TypeAlias = str | Exception

@deprecated("`docutils.utils.error_reporting` module is deprecated and will be removed in Docutils 0.21 or later.")
class SafeString:
    """
    A wrapper providing robust conversion to `str` and `unicode`.
    """

    data: object
    encoding: str
    encoding_errors: str
    decoding_errors: str
    def __init__(
        self,
        data: object,
        encoding: str | None = None,
        encoding_errors: str = "backslashreplace",
        decoding_errors: str = "replace",
    ) -> None: ...
    def __unicode__(self) -> str:
        """
        Return unicode representation of `self.data`.

        Try ``unicode(self.data)``, catch `UnicodeError` and

        * if `self.data` is an Exception instance, work around
          http://bugs.python.org/issue2517 with an emulation of
          Exception.__unicode__,

        * else decode with `self.encoding` and `self.decoding_errors`.
        """

@deprecated("`docutils.utils.error_reporting` module is deprecated and will be removed in Docutils 0.21 or later.")
class ErrorString(SafeString):
    """
    Safely report exception type and message.
    """

@deprecated("`docutils.utils.error_reporting` module is deprecated and will be removed in Docutils 0.21 or later.")
class ErrorOutput:
    """
    Wrapper class for file-like error streams with
    failsafe de- and encoding of `str`, `bytes`, `unicode` and
    `Exception` instances.
    """

    stream: TextIO | TextIOWrapper
    encoding: str
    encoding_errors: str
    decoding_errors: str
    def __init__(
        self,
        stream=None,
        encoding: str | None = None,
        encoding_errors: str = "backslashreplace",
        decoding_errors: str = "replace",
    ) -> None:
        """
        :Parameters:
            - `stream`: a file-like object,
                        a string (path to a file),
                        `None` (write to `sys.stderr`, default), or
                        evaluating to `False` (write() requests are ignored).
            - `encoding`: `stream` text encoding. Guessed if None.
            - `encoding_errors`: how to treat encoding errors.
        """

    def write(self, data: _DataType) -> None:
        """
        Write `data` to self.stream. Ignore, if self.stream is False.

        `data` can be a `string`, `unicode`, or `Exception` instance.
        """

    def close(self) -> None:
        """
        Close the error-output stream.

        Ignored if the stream is` sys.stderr` or `sys.stdout` or has no
        close() method.
        """
