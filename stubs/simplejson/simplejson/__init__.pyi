"""JSON (JavaScript Object Notation) <http://json.org> is a subset of
JavaScript syntax (ECMA-262 3rd edition) used as a lightweight data
interchange format.

:mod:`simplejson` exposes an API familiar to users of the standard library
:mod:`marshal` and :mod:`pickle` modules. It is the externally maintained
version of the :mod:`json` library contained in Python 2.6, but maintains
compatibility back to Python 2.5 and (currently) has significant performance
advantages, even without using the optional C extension for speedups.

Encoding basic Python object hierarchies::

    >>> import simplejson as json
    >>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    >>> print(json.dumps("\\"foo\\bar"))
    "\\"foo\\bar"
    >>> print(json.dumps(u'\\u1234'))
    "\\u1234"
    >>> print(json.dumps('\\\\'))
    "\\\\"
    >>> print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
    {"a": 0, "b": 0, "c": 0}
    >>> from simplejson.compat import StringIO
    >>> io = StringIO()
    >>> json.dump(['streaming API'], io)
    >>> io.getvalue()
    '["streaming API"]'

Compact encoding::

    >>> import simplejson as json
    >>> obj = [1,2,3,{'4': 5, '6': 7}]
    >>> json.dumps(obj, separators=(',',':'), sort_keys=True)
    '[1,2,3,{"4":5,"6":7}]'

Pretty printing::

    >>> import simplejson as json
    >>> print(json.dumps({'4': 5, '6': 7}, sort_keys=True, indent='    '))
    {
        "4": 5,
        "6": 7
    }

Decoding JSON::

    >>> import simplejson as json
    >>> obj = [u'foo', {u'bar': [u'baz', None, 1.0, 2]}]
    >>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]') == obj
    True
    >>> json.loads('"\\\\"foo\\\\bar"') == u'"foo\\x08ar'
    True
    >>> from simplejson.compat import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> json.load(io)[0] == 'streaming API'
    True

Specializing JSON object decoding::

    >>> import simplejson as json
    >>> def as_complex(dct):
    ...     if '__complex__' in dct:
    ...         return complex(dct['real'], dct['imag'])
    ...     return dct
    ...
    >>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
    ...     object_hook=as_complex)
    (1+2j)
    >>> from decimal import Decimal
    >>> json.loads('1.1', parse_float=Decimal) == Decimal('1.1')
    True

Specializing JSON object encoding::

    >>> import simplejson as json
    >>> def encode_complex(obj):
    ...     if isinstance(obj, complex):
    ...         return [obj.real, obj.imag]
    ...     raise TypeError('Object of type %s is not JSON serializable' %
    ...                     obj.__class__.__name__)
    ...
    >>> json.dumps(2 + 1j, default=encode_complex)
    '[2.0, 1.0]'
    >>> json.JSONEncoder(default=encode_complex).encode(2 + 1j)
    '[2.0, 1.0]'
    >>> ''.join(json.JSONEncoder(default=encode_complex).iterencode(2 + 1j))
    '[2.0, 1.0]'

Using simplejson.tool from the shell to validate and pretty-print::

    $ echo '{"json":"obj"}' | python -m simplejson.tool
    {
        "json": "obj"
    }
    $ echo '{ 1.2:3.4}' | python -m simplejson.tool
    Expecting property name: line 1 column 3 (char 2)

Parsing multiple documents serialized as JSON lines (newline-delimited JSON)::

    >>> import simplejson as json
    >>> def loads_lines(docs):
    ...     for doc in docs.splitlines():
    ...         yield json.loads(doc)
    ...
    >>> sum(doc["count"] for doc in loads_lines('{"count":1}\\n{"count":2}\\n{"count":3}\\n'))
    6

Serializing multiple objects to JSON lines (newline-delimited JSON)::

    >>> import simplejson as json
    >>> def dumps_lines(objs):
    ...     for obj in objs:
    ...         yield json.dumps(obj, separators=(',',':')) + '\\n'
    ...
    >>> ''.join(dumps_lines([{'count': 1}, {'count': 2}, {'count': 3}]))
    '{"count":1}\\n{"count":2}\\n{"count":3}\\n'

"""

from _typeshed import SupportsRichComparison
from collections import OrderedDict
from collections.abc import Callable
from typing import IO, Any, TypeVar, overload
from typing_extensions import TypeAlias

from simplejson.decoder import JSONDecoder as JSONDecoder
from simplejson.encoder import JSONEncoder as JSONEncoder, JSONEncoderForHTML as JSONEncoderForHTML
from simplejson.raw_json import RawJSON as RawJSON
from simplejson.scanner import JSONDecodeError as JSONDecodeError

_LoadsString: TypeAlias = str | bytes | bytearray
_T = TypeVar("_T")

@overload
def dumps(
    obj: Any,
    skipkeys: bool = ...,
    ensure_ascii: bool = ...,
    check_circular: bool = ...,
    allow_nan: bool = ...,
    *,
    cls: type[JSONEncoder],
    indent: str | int | None = ...,
    separators: tuple[str, str] | None = ...,
    encoding: str | None = ...,
    default: Callable[[Any], Any] | None = ...,
    use_decimal: bool = ...,
    namedtuple_as_object: bool = ...,
    tuple_as_array: bool = ...,
    bigint_as_string: bool = ...,
    sort_keys: bool = ...,
    item_sort_key: Callable[[Any], SupportsRichComparison] | None = ...,
    for_json: bool = ...,
    ignore_nan: bool = ...,
    int_as_string_bitcount: int | None = ...,
    iterable_as_array: bool = ...,
    **kw: Any,
) -> str:
    """Serialize ``obj`` to a JSON formatted ``str``.

    If ``skipkeys`` is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``long``, ``float``, ``bool``, ``None``)
    will be skipped instead of raising a ``TypeError``.

    If *ensure_ascii* is false (default: ``True``), then the output may
    contain non-ASCII characters, so long as they do not need to be escaped
    by JSON. When it is true, all non-ASCII characters are escaped.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If *allow_nan* is true (default: ``False``), then out of range ``float``
    values (``nan``, ``inf``, ``-inf``) will be serialized to
    their JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``)
    instead of raising a ValueError. See
    *ignore_nan* for ECMA-262 compliant behavior.

    If ``indent`` is a string, then JSON array elements and object members
    will be pretty-printed with a newline followed by that string repeated
    for each level of nesting. ``None`` (the default) selects the most compact
    representation without any newlines. For backwards compatibility with
    versions of simplejson earlier than 2.1.0, an integer is also accepted
    and is converted to a string with that many spaces.

    If specified, ``separators`` should be an
    ``(item_separator, key_separator)`` tuple.  The default is ``(', ', ': ')``
    if *indent* is ``None`` and ``(',', ': ')`` otherwise.  To get the most
    compact JSON representation, you should specify ``(',', ':')`` to eliminate
    whitespace.

    ``encoding`` is the character encoding for bytes instances, default is
    UTF-8.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    If *use_decimal* is true (default: ``True``) then decimal.Decimal
    will be natively serialized to JSON with full precision.

    If *namedtuple_as_object* is true (default: ``True``),
    :class:`tuple` subclasses with ``_asdict()`` methods will be encoded
    as JSON objects.

    If *tuple_as_array* is true (default: ``True``),
    :class:`tuple` (and subclasses) will be encoded as JSON arrays.

    If *iterable_as_array* is true (default: ``False``),
    any object not in the above table that implements ``__iter__()``
    will be encoded as a JSON array.

    If *bigint_as_string* is true (not the default), ints 2**53 and higher
    or lower than -2**53 will be encoded as strings. This is to avoid the
    rounding that happens in Javascript otherwise.

    If *int_as_string_bitcount* is a positive number (n), then int of size
    greater than or equal to 2**n or lower than or equal to -2**n will be
    encoded as strings.

    If specified, *item_sort_key* is a callable used to sort the items in
    each dictionary. This is useful if you want to sort items other than
    in alphabetical order by key. This option takes precedence over
    *sort_keys*.

    If *sort_keys* is true (default: ``False``), the output of dictionaries
    will be sorted by item.

    If *for_json* is true (default: ``False``), objects with a ``for_json()``
    method will use the return value of that method for encoding as JSON
    instead of the object.

    If *ignore_nan* is true (default: ``False``), then out of range
    :class:`float` values (``nan``, ``inf``, ``-inf``) will be serialized as
    ``null`` in compliance with the ECMA-262 specification. If true, this will
    override *allow_nan*.

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg. NOTE: You should use *default* instead of subclassing
    whenever possible.

    """

@overload
def dumps(
    obj: Any,
    skipkeys: bool = ...,
    ensure_ascii: bool = ...,
    check_circular: bool = ...,
    allow_nan: bool = ...,
    cls: type[JSONEncoder] | None = ...,
    indent: str | int | None = ...,
    separators: tuple[str, str] | None = ...,
    encoding: str | None = ...,
    default: Callable[[Any], Any] | None = ...,
    use_decimal: bool = ...,
    namedtuple_as_object: bool = ...,
    tuple_as_array: bool = ...,
    bigint_as_string: bool = ...,
    sort_keys: bool = ...,
    item_sort_key: Callable[[Any], SupportsRichComparison] | None = ...,
    for_json: bool = ...,
    ignore_nan: bool = ...,
    int_as_string_bitcount: int | None = ...,
    iterable_as_array: bool = ...,
) -> str: ...
@overload
def dump(
    obj: Any,
    fp: IO[str],
    skipkeys: bool = ...,
    ensure_ascii: bool = ...,
    check_circular: bool = ...,
    allow_nan: bool = ...,
    *,
    cls: type[JSONEncoder],
    indent: str | int | None = ...,
    separators: tuple[str, str] | None = ...,
    encoding: str | None = ...,
    default: Callable[[Any], Any] | None = ...,
    use_decimal: bool = ...,
    namedtuple_as_object: bool = ...,
    tuple_as_array: bool = ...,
    bigint_as_string: bool = ...,
    sort_keys: bool = ...,
    item_sort_key: Callable[[Any], SupportsRichComparison] | None = ...,
    for_json: bool = ...,
    ignore_nan: bool = ...,
    int_as_string_bitcount: int | None = ...,
    iterable_as_array: bool = ...,
    **kw: Any,
) -> None:
    """Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    If *skipkeys* is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``long``, ``float``, ``bool``, ``None``)
    will be skipped instead of raising a ``TypeError``.

    If *ensure_ascii* is false (default: ``True``), then the output may
    contain non-ASCII characters, so long as they do not need to be escaped
    by JSON. When it is true, all non-ASCII characters are escaped.

    If *allow_nan* is true (default: ``False``), then out of range ``float``
    values (``nan``, ``inf``, ``-inf``) will be serialized to
    their JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``)
    instead of raising a ValueError. See
    *ignore_nan* for ECMA-262 compliant behavior.

    If *indent* is a string, then JSON array elements and object members
    will be pretty-printed with a newline followed by that string repeated
    for each level of nesting. ``None`` (the default) selects the most compact
    representation without any newlines.

    If specified, *separators* should be an
    ``(item_separator, key_separator)`` tuple.  The default is ``(', ', ': ')``
    if *indent* is ``None`` and ``(',', ': ')`` otherwise.  To get the most
    compact JSON representation, you should specify ``(',', ':')`` to eliminate
    whitespace.

    *encoding* is the character encoding for str instances, default is UTF-8.

    *default(obj)* is a function that should return a serializable version
    of obj or raise ``TypeError``. The default simply raises ``TypeError``.

    If *use_decimal* is true (default: ``True``) then decimal.Decimal
    will be natively serialized to JSON with full precision.

    If *namedtuple_as_object* is true (default: ``True``),
    :class:`tuple` subclasses with ``_asdict()`` methods will be encoded
    as JSON objects.

    If *tuple_as_array* is true (default: ``True``),
    :class:`tuple` (and subclasses) will be encoded as JSON arrays.

    If *iterable_as_array* is true (default: ``False``),
    any object not in the above table that implements ``__iter__()``
    will be encoded as a JSON array.

    If *bigint_as_string* is true (default: ``False``), ints 2**53 and higher
    or lower than -2**53 will be encoded as strings. This is to avoid the
    rounding that happens in Javascript otherwise. Note that this is still a
    lossy operation that will not round-trip correctly and should be used
    sparingly.

    If *int_as_string_bitcount* is a positive number (n), then int of size
    greater than or equal to 2**n or lower than or equal to -2**n will be
    encoded as strings.

    If specified, *item_sort_key* is a callable used to sort the items in
    each dictionary. This is useful if you want to sort items other than
    in alphabetical order by key. This option takes precedence over
    *sort_keys*.

    If *sort_keys* is true (default: ``False``), the output of dictionaries
    will be sorted by item.

    If *for_json* is true (default: ``False``), objects with a ``for_json()``
    method will use the return value of that method for encoding as JSON
    instead of the object.

    If *ignore_nan* is true (default: ``False``), then out of range
    :class:`float` values (``nan``, ``inf``, ``-inf``) will be serialized as
    ``null`` in compliance with the ECMA-262 specification. If true, this will
    override *allow_nan*.

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg. NOTE: You should use *default* or *for_json* instead
    of subclassing whenever possible.

    """

@overload
def dump(
    obj: Any,
    fp: IO[str],
    skipkeys: bool = ...,
    ensure_ascii: bool = ...,
    check_circular: bool = ...,
    allow_nan: bool = ...,
    cls: type[JSONEncoder] | None = ...,
    indent: str | int | None = ...,
    separators: tuple[str, str] | None = ...,
    encoding: str | None = ...,
    default: Callable[[Any], Any] | None = ...,
    use_decimal: bool = ...,
    namedtuple_as_object: bool = ...,
    tuple_as_array: bool = ...,
    bigint_as_string: bool = ...,
    sort_keys: bool = ...,
    item_sort_key: Callable[[Any], SupportsRichComparison] | None = ...,
    for_json: bool = ...,
    ignore_nan: bool = ...,
    int_as_string_bitcount: int | None = ...,
    iterable_as_array: bool = ...,
) -> None: ...
@overload
def loads(
    s: _LoadsString,
    encoding: str | None = ...,
    *,
    cls: type[JSONDecoder],
    object_hook: Callable[[dict[Any, Any]], Any] | None = ...,
    parse_float: Callable[[str], Any] | None = ...,
    parse_int: Callable[[str], Any] | None = ...,
    parse_constant: Callable[[str], Any] | None = ...,
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = ...,
    use_decimal: bool = ...,
    allow_nan: bool = ...,
    **kw: Any,
) -> Any:
    """Deserialize ``s`` (a ``str`` or ``unicode`` instance containing a JSON
    document) to a Python object.

    *encoding* determines the encoding used to interpret any
    :class:`bytes` objects decoded by this instance (``'utf-8'`` by
    default). It has no effect when decoding :class:`unicode` objects.

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
    accept the non-standard floats ``NaN``, ``Infinity``, and ``-Infinity``
    and enable the use of the deprecated *parse_constant*.

    If *use_decimal* is true (default: ``False``) then it implies
    parse_float=decimal.Decimal for parity with ``dump``.

    *parse_constant*, if specified, will be
    called with one of the following strings: ``'-Infinity'``,
    ``'Infinity'``, ``'NaN'``. It is not recommended to use this feature,
    as it is rare to parse non-compliant JSON containing these values.

    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg. NOTE: You should use *object_hook* or *object_pairs_hook* instead
    of subclassing whenever possible.

    """

@overload
def loads(
    s: _LoadsString,
    encoding: str | None = ...,
    cls: type[JSONDecoder] | None = ...,
    object_hook: Callable[[dict[Any, Any]], Any] | None = ...,
    parse_float: Callable[[str], Any] | None = ...,
    parse_int: Callable[[str], Any] | None = ...,
    parse_constant: Callable[[str], Any] | None = ...,
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = ...,
    use_decimal: bool = ...,
    allow_nan: bool = ...,
) -> Any: ...
@overload
def load(
    fp: IO[str],
    encoding: str | None = ...,
    *,
    cls: type[JSONDecoder],
    object_hook: Callable[[dict[Any, Any]], Any] | None = ...,
    parse_float: Callable[[str], Any] | None = ...,
    parse_int: Callable[[str], Any] | None = ...,
    parse_constant: Callable[[str], Any] | None = ...,
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = ...,
    use_decimal: bool = ...,
    allow_nan: bool = ...,
    **kw: Any,
) -> Any:
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document as `str` or `bytes`) to a Python object.

    *encoding* determines the encoding used to interpret any
    `bytes` objects decoded by this instance (``'utf-8'`` by
    default). It has no effect when decoding `str` objects.

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
    JSON float to be decoded. By default, this is equivalent to
    ``float(num_str)``. This can be used to use another datatype or parser
    for JSON floats (e.g. :class:`decimal.Decimal`).

    *parse_int*, if specified, will be called with the string of every
    JSON int to be decoded. By default, this is equivalent to
    ``int(num_str)``.  This can be used to use another datatype or parser
    for JSON integers (e.g. :class:`float`).

    *allow_nan*, if True (default false), will allow the parser to
    accept the non-standard floats ``NaN``, ``Infinity``, and ``-Infinity``
    and enable the use of the deprecated *parse_constant*.

    If *use_decimal* is true (default: ``False``) then it implies
    parse_float=decimal.Decimal for parity with ``dump``.

    *parse_constant*, if specified, will be
    called with one of the following strings: ``'-Infinity'``,
    ``'Infinity'``, ``'NaN'``. It is not recommended to use this feature,
    as it is rare to parse non-compliant JSON containing these values.

    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg. NOTE: You should use *object_hook* or *object_pairs_hook* instead
    of subclassing whenever possible.

    """

@overload
def load(
    fp: IO[str],
    encoding: str | None = ...,
    cls: type[JSONDecoder] | None = ...,
    object_hook: Callable[[dict[Any, Any]], Any] | None = ...,
    parse_float: Callable[[str], Any] | None = ...,
    parse_int: Callable[[str], Any] | None = ...,
    parse_constant: Callable[[str], Any] | None = ...,
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = ...,
    use_decimal: bool = ...,
    allow_nan: bool = ...,
) -> Any: ...
def simple_first(kv: tuple[_T, object]) -> tuple[bool, _T]:
    """Helper function to pass to item_sort_key to sort simple
    elements to the top, then container elements.
    """

__all__ = [
    "dump",
    "dumps",
    "load",
    "loads",
    "JSONDecoder",
    "JSONDecodeError",
    "JSONEncoder",
    "OrderedDict",
    "simple_first",
    "RawJSON",
]
