"""Implementation of JSONDecoder"""

from collections.abc import Callable
from re import Match
from typing import Any, Literal

class JSONDecoder:
    """Simple JSON <http://json.org> decoder

    Performs the following translations in decoding by default:

    +---------------+-------------------+
    | JSON          | Python            |
    +===============+===================+
    | object        | dict              |
    +---------------+-------------------+
    | array         | list              |
    +---------------+-------------------+
    | string        | str, unicode      |
    +---------------+-------------------+
    | number (int)  | int, long         |
    +---------------+-------------------+
    | number (real) | float             |
    +---------------+-------------------+
    | true          | True              |
    +---------------+-------------------+
    | false         | False             |
    +---------------+-------------------+
    | null          | None              |
    +---------------+-------------------+

    When allow_nan=True, it also understands
    ``NaN``, ``Infinity``, and ``-Infinity`` as
    their corresponding ``float`` values, which is outside the JSON spec.

    """

    encoding: str
    object_hook: Callable[[dict[Any, Any]], Any] | None
    parse_float: Callable[[str], Any] | None
    parse_int: Callable[[str], Any] | None
    parse_constant: Callable[[str], Any] | None
    strict: bool
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None
    memo: dict[Any, Any]
    scan_once: Callable[[str, int], tuple[bool, int]]

    def __init__(
        self,
        encoding: str | None = ...,
        object_hook: Callable[[dict[Any, Any]], Any] | None = ...,
        parse_float: Callable[[str], Any] | None = ...,
        parse_int: Callable[[str], Any] | None = ...,
        parse_constant: Callable[[str], Any] | None = ...,
        strict: bool = ...,
        object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = ...,
        allow_nan: bool = ...,
    ) -> None:
        """
        *encoding* determines the encoding used to interpret any
        :class:`str` objects decoded by this instance (``'utf-8'`` by
        default).  It has no effect when decoding :class:`unicode` objects.

        Note that currently only encodings that are a superset of ASCII work,
        strings of other encodings should be passed in as :class:`unicode`.

        *object_hook*, if specified, will be called with the result of every
        JSON object decoded and its return value will be used in place of the
        given :class:`dict`.  This can be used to provide custom
        deserializations (e.g. to support JSON-RPC class hinting).

        *object_pairs_hook* is an optional function that will be called with
        the result of any object literal decode with an ordered list of pairs.
        The return value of *object_pairs_hook* will be used instead of the
        :class:`dict`.  This feature can be used to implement custom decoders
        that rely on the order that the key and value pairs are decoded (for
        example, :func:`collections.OrderedDict` will remember the order of
        insertion). If *object_hook* is also defined, the *object_pairs_hook*
        takes priority.

        *parse_float*, if specified, will be called with the string of every
        JSON float to be decoded.  By default, this is equivalent to
        ``float(num_str)``. This can be used to use another datatype or parser
        for JSON floats (e.g. :class:`decimal.Decimal`).

        *parse_int*, if specified, will be called with the string of every
        JSON int to be decoded.  By default, this is equivalent to
        ``int(num_str)``.  This can be used to use another datatype or parser
        for JSON integers (e.g. :class:`float`).

        *allow_nan*, if True (default false), will allow the parser to
        accept the non-standard floats ``NaN``, ``Infinity``, and ``-Infinity``.

        *parse_constant*, if specified, will be
        called with one of the following strings: ``'-Infinity'``,
        ``'Infinity'``, ``'NaN'``. It is not recommended to use this feature,
        as it is rare to parse non-compliant JSON containing these values.

        *strict* controls the parser's behavior when it encounters an
        invalid control character in a string. The default setting of
        ``True`` means that unescaped control characters are parse errors, if
        ``False`` then control characters will be allowed in strings.

        """

    def decode(self, s: str, _w: Callable[[str, int], Match[str]] = ..., _PY3: Literal[True] = ...) -> Any:
        """Return the Python representation of ``s`` (a ``str`` or ``unicode``
        instance containing a JSON document)

        """

    def raw_decode(
        self, s: str, idx: int = ..., _w: Callable[[str, int], Match[str]] = ..., _PY3: Literal[True] = ...
    ) -> tuple[Any, int]:
        """Decode a JSON document from ``s`` (a ``str`` or ``unicode``
        beginning with a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.
        Optionally, ``idx`` can be used to specify an offset in ``s`` where
        the JSON document begins.

        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.

        """

__all__ = ["JSONDecoder"]
