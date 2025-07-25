"""
Parse four ``Accept*`` headers used in server-driven content negotiation.

The four headers are ``Accept``, ``Accept-Charset``, ``Accept-Encoding`` and
``Accept-Language``.
"""

from _typeshed import SupportsItems
from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import Any, Literal, NamedTuple, Protocol, TypeVar, overload
from typing_extensions import Self, TypeAlias

from webob._types import AsymmetricPropertyWithDelete

_T = TypeVar("_T")
_ListOrTuple: TypeAlias = list[_T] | tuple[_T, ...]
_ParsedAccept: TypeAlias = tuple[str, float, list[tuple[str, str]], list[str | tuple[str, str]]]

class _SupportsStr(Protocol):
    def __str__(self) -> str: ...  # noqa: Y029

_AnyAcceptHeader: TypeAlias = AcceptValidHeader | AcceptInvalidHeader | AcceptNoHeader
_AnyAcceptCharsetHeader: TypeAlias = AcceptCharsetValidHeader | AcceptCharsetInvalidHeader | AcceptCharsetNoHeader
_AnyAcceptEncodingHeader: TypeAlias = AcceptEncodingValidHeader | AcceptEncodingInvalidHeader | AcceptEncodingNoHeader
_AnyAcceptLanguageHeader: TypeAlias = AcceptLanguageValidHeader | AcceptLanguageInvalidHeader | AcceptLanguageNoHeader

_AcceptProperty: TypeAlias = AsymmetricPropertyWithDelete[
    _AnyAcceptHeader,
    (
        _AnyAcceptHeader
        | SupportsItems[str, float | tuple[float, str]]
        | _ListOrTuple[str | tuple[str, float, str] | list[Any]]
        | _SupportsStr
        | str
        | None
    ),
]
_AcceptCharsetProperty: TypeAlias = AsymmetricPropertyWithDelete[
    _AnyAcceptCharsetHeader,
    (
        _AnyAcceptCharsetHeader
        | SupportsItems[str, float]
        | _ListOrTuple[str | tuple[str, float] | list[Any]]
        | _SupportsStr
        | str
        | None
    ),
]
_AcceptEncodingProperty: TypeAlias = AsymmetricPropertyWithDelete[
    _AnyAcceptEncodingHeader,
    (
        _AnyAcceptEncodingHeader
        | SupportsItems[str, float]
        | _ListOrTuple[str | tuple[str, float] | list[Any]]
        | _SupportsStr
        | str
        | None
    ),
]
_AcceptLanguageProperty: TypeAlias = AsymmetricPropertyWithDelete[
    _AnyAcceptLanguageHeader,
    (
        _AnyAcceptLanguageHeader
        | SupportsItems[str, float]
        | _ListOrTuple[str | tuple[str, float] | list[Any]]
        | _SupportsStr
        | str
        | None
    ),
]

class AcceptOffer(NamedTuple):
    """
    A pre-parsed offer tuple represeting a value in the format
    ``type/subtype;param0=value0;param1=value1``.

    :ivar type: The media type's root category.
    :ivar subtype: The media type's subtype.
    :ivar params: A tuple of 2-tuples containing parameter names and values.

    """

    type: str
    subtype: str
    params: tuple[tuple[str, str], ...]

class Accept:
    """
    Represent an ``Accept`` header.

    Base class for :class:`AcceptValidHeader`, :class:`AcceptNoHeader`, and
    :class:`AcceptInvalidHeader`.
    """

    @classmethod
    def parse(cls, value: str) -> Iterator[_ParsedAccept]:
        """
        Parse an ``Accept`` header.

        :param value: (``str``) header value
        :return: If `value` is a valid ``Accept`` header, returns an iterator
                 of (*media_range*, *qvalue*, *media_type_params*,
                 *extension_params*) tuples, as parsed from the header from
                 left to right.

                 | *media_range* is the media range, including any media type
                   parameters. The media range is returned in a canonicalised
                   form (except the case of the characters are unchanged):
                   unnecessary spaces around the semicolons before media type
                   parameters are removed; the parameter values are returned in
                   a form where only the '``\\``' and '``"``' characters are
                   escaped, and the values are quoted with double quotes only
                   if they need to be quoted.

                 | *qvalue* is the quality value of the media range.

                 | *media_type_params* is the media type parameters, as a list
                   of (parameter name, value) tuples.

                 | *extension_params* is the extension parameters, as a list
                   where each item is either a parameter string or a (parameter
                   name, value) tuple.
        :raises ValueError: if `value` is an invalid header
        """

    @classmethod
    def parse_offer(cls, offer: str | AcceptOffer) -> AcceptOffer:
        """
        Parse an offer into its component parts.

        :param offer: A media type or range in the format
                      ``type/subtype[;params]``.
        :return: A named tuple containing ``(*type*, *subtype*, *params*)``.

                 | *params* is a list containing ``(*parameter name*, *value*)``
                   values.

        :raises ValueError: If the offer does not match the required format.

        """

class AcceptValidHeader(Accept):
    """
    Represent a valid ``Accept`` header.

    A valid header is one that conforms to :rfc:`RFC 7231, section 5.3.2
    <7231#section-5.3.2>`.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptValidHeader.__add__`).
    """

    @property
    def header_value(self) -> str:
        """(``str`` or ``None``) The header value."""

    @property
    def parsed(self) -> list[_ParsedAccept]:
        """
        (``list`` or ``None``) Parsed form of the header.

        A list of (*media_range*, *qvalue*, *media_type_params*,
        *extension_params*) tuples, where

        *media_range* is the media range, including any media type parameters.
        The media range is returned in a canonicalised form (except the case of
        the characters are unchanged): unnecessary spaces around the semicolons
        before media type parameters are removed; the parameter values are
        returned in a form where only the '``\\``' and '``"``' characters are
        escaped, and the values are quoted with double quotes only if they need
        to be quoted.

        *qvalue* is the quality value of the media range.

        *media_type_params* is the media type parameters, as a list of
        (parameter name, value) tuples.

        *extension_params* is the extension parameters, as a list where each
        item is either a parameter string or a (parameter name, value) tuple.
        """

    def __init__(self, header_value: str) -> None:
        """
        Create an :class:`AcceptValidHeader` instance.

        :param header_value: (``str``) header value.
        :raises ValueError: if `header_value` is an invalid value for an
                            ``Accept`` header.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    def __add__(
        self,
        other: (
            _AnyAcceptHeader
            | SupportsItems[str, float | tuple[float, str]]
            | _ListOrTuple[str | tuple[str, float, str] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, with media ranges ``str``'s (including any media type
          parameters) as keys, and either qvalues ``float``'s or (*qvalues*,
          *extension_params*) tuples as values, where *extension_params* is a
          ``str`` of the extension parameters segment of the header element,
          starting with the first '``;``'
        * a ``tuple`` or ``list``, where each item is either a header element
          ``str``, or a (*media_range*, *qvalue*, *extension_params*) ``tuple``
          or ``list`` where *media_range* is a ``str`` of the media range
          including any media type parameters, and *extension_params* is a
          ``str`` of the extension parameters segment of the header element,
          starting with the first '``;``'
        * an :class:`AcceptValidHeader`, :class:`AcceptNoHeader`, or
          :class:`AcceptInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or another
        :class:`AcceptValidHeader` instance, and the header value it represents
        is not `''`, then the two header values are joined with ``', '``, and a
        new :class:`AcceptValidHeader` instance with the new header value is
        returned.

        If `other` is a valid header value or another
        :class:`AcceptValidHeader` instance representing a header value of
        `''`; or if it is ``None`` or an :class:`AcceptNoHeader` instance; or
        if it is an invalid header value, or an :class:`AcceptInvalidHeader`
        instance, then a new :class:`AcceptValidHeader` instance with the same
        header value as ``self`` is returned.
        """

    def __bool__(self) -> Literal[True]:
        """
        Return whether ``self`` represents a valid ``Accept`` header.

        Return ``True`` if ``self`` represents a valid header, and ``False`` if
        it represents an invalid header, or the header not being in the
        request.

        For this class, it always returns ``True``.
        """

    def __contains__(self, offer: str) -> bool:
        """
        Return ``bool`` indicating whether `offer` is acceptable.

        .. warning::

           The behavior of :meth:`AcceptValidHeader.__contains__` is currently
           being maintained for backward compatibility, but it will change in
           the future to better conform to the RFC.

        :param offer: (``str``) media type offer
        :return: (``bool``) Whether ``offer`` is acceptable according to the
                 header.

        This uses the old criterion of a match in
        :meth:`AcceptValidHeader._old_match`, which is not as specified in
        :rfc:`RFC 7231, section 5.3.2 <7231#section-5.3.2>`. It does not
        correctly take into account media type parameters:

            >>> 'text/html;p=1' in AcceptValidHeader('text/html')
            False

        or media ranges with ``q=0`` in the header::

            >>> 'text/html' in AcceptValidHeader('text/*, text/html;q=0')
            True
            >>> 'text/html' in AcceptValidHeader('text/html;q=0, */*')
            True

        (See the docstring for :meth:`AcceptValidHeader._old_match` for other
        problems with the old criterion for matching.)
        """

    def __iter__(self) -> Iterator[str]:
        """
        Return all the ranges with non-0 qvalues, in order of preference.

        .. warning::

           The behavior of this method is currently maintained for backward
           compatibility, but will change in the future.

        :return: iterator of all the media ranges in the header with non-0
                 qvalues, in descending order of qvalue. If two ranges have the
                 same qvalue, they are returned in the order of their positions
                 in the header, from left to right.

        Please note that this is a simple filter for the ranges in the header
        with non-0 qvalues, and is not necessarily the same as what the client
        prefers, e.g. ``'audio/basic;q=0, */*'`` means 'everything but
        audio/basic', but ``list(instance)`` would return only ``['*/*']``.
        """

    def __radd__(
        self,
        other: (
            _AnyAcceptHeader
            | SupportsItems[str, float | tuple[float, str]]
            | _ListOrTuple[str | tuple[str, float, str] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptValidHeader.__add__`.
        """

    def accept_html(self) -> bool:
        """
        Return ``True`` if any HTML-like type is accepted.

        The HTML-like types are 'text/html', 'application/xhtml+xml',
        'application/xml' and 'text/xml'.
        """

    @property
    def accepts_html(self) -> bool:
        """
        Return ``True`` if any HTML-like type is accepted.

        The HTML-like types are 'text/html', 'application/xhtml+xml',
        'application/xml' and 'text/xml'.
        """

    def acceptable_offers(self, offers: Sequence[str]) -> list[tuple[str, float]]:
        """
        Return the offers that are acceptable according to the header.

        The offers are returned in descending order of preference, where
        preference is indicated by the qvalue of the media range in the header
        that best matches the offer.

        This uses the matching rules described in :rfc:`RFC 7231, section 5.3.2
        <7231#section-5.3.2>`.

        Any offers that cannot be parsed via
        :meth:`.Accept.parse_offer` will be ignored.

        :param offers: ``iterable`` of ``str`` media types (media types can
                       include media type parameters) or pre-parsed instances
                       of :class:`.AcceptOffer`.
        :return: A list of tuples of the form (media type, qvalue), in
                 descending order of qvalue. Where two offers have the same
                 qvalue, they are returned in the same order as their order in
                 `offers`.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: None = None) -> str | None:
        """
        Return the best match from the sequence of media type `offers`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future.

           :meth:`AcceptValidHeader.best_match` uses its own algorithm (one not
           specified in :rfc:`RFC 7231 <7231>`) to determine what is a best
           match. The algorithm has many issues, and does not conform to
           :rfc:`RFC 7231 <7231>`.

        Each media type in `offers` is checked against each non-``q=0`` range
        in the header. If the two are a match according to WebOb's old
        criterion for a match, the quality value of the match is the qvalue of
        the media range from the header multiplied by the server quality value
        of the offer (if the server quality value is not supplied, it is 1).

        The offer in the match with the highest quality value is the best
        match. If there is more than one match with the highest qvalue, the
        match where the media range has a lower number of '*'s is the best
        match. If the two have the same number of '*'s, the one that shows up
        first in `offers` is the best match.

        :param offers: (iterable)

                       | Each item in the iterable may be a ``str`` media type,
                         or a (media type, server quality value) ``tuple`` or
                         ``list``. (The two may be mixed in the iterable.)

        :param default_match: (optional, any type) the value to be returned if
                              there is no match

        :return: (``str``, or the type of `default_match`)

                 | The offer that is the best match. If there is no match, the
                   value of `default_match` is returned.

        This uses the old criterion of a match in
        :meth:`AcceptValidHeader._old_match`, which is not as specified in
        :rfc:`RFC 7231, section 5.3.2 <7231#section-5.3.2>`. It does not
        correctly take into account media type parameters:

            >>> instance = AcceptValidHeader('text/html')
            >>> instance.best_match(offers=['text/html;p=1']) is None
            True

        or media ranges with ``q=0`` in the header::

            >>> instance = AcceptValidHeader('text/*, text/html;q=0')
            >>> instance.best_match(offers=['text/html'])
            'text/html'

            >>> instance = AcceptValidHeader('text/html;q=0, */*')
            >>> instance.best_match(offers=['text/html'])
            'text/html'

        (See the docstring for :meth:`AcceptValidHeader._old_match` for other
        problems with the old criterion for matching.)

        Another issue is that this method considers the best matching range for
        an offer to be the matching range with the highest quality value,
        (where quality values are tied, the most specific media range is
        chosen); whereas :rfc:`RFC 7231, section 5.3.2 <7231#section-5.3.2>`
        specifies that we should consider the best matching range for a media
        type offer to be the most specific matching range.::

            >>> instance = AcceptValidHeader('text/html;q=0.5, text/*')
            >>> instance.best_match(offers=['text/html', 'text/plain'])
            'text/html'
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: str) -> str: ...
    def quality(self, offer: str) -> float | None:
        """
        Return quality value of given offer, or ``None`` if there is no match.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future.

        :param offer: (``str``) media type offer
        :return: (``float`` or ``None``)

                 | The highest quality value from the media range(s) that match
                   the `offer`, or ``None`` if there is no match.

        This uses the old criterion of a match in
        :meth:`AcceptValidHeader._old_match`, which is not as specified in
        :rfc:`RFC 7231, section 5.3.2 <7231#section-5.3.2>`. It does not
        correctly take into account media type parameters:

            >>> instance = AcceptValidHeader('text/html')
            >>> instance.quality('text/html;p=1') is None
            True

        or media ranges with ``q=0`` in the header::

            >>> instance = AcceptValidHeader('text/*, text/html;q=0')
            >>> instance.quality('text/html')
            1.0
            >>> AcceptValidHeader('text/html;q=0, */*').quality('text/html')
            1.0

        (See the docstring for :meth:`AcceptValidHeader._old_match` for other
        problems with the old criterion for matching.)

        Another issue is that this method considers the best matching range for
        an offer to be the matching range with the highest quality value,
        whereas :rfc:`RFC 7231, section 5.3.2 <7231#section-5.3.2>` specifies
        that we should consider the best matching range for a media type offer
        to be the most specific matching range.::

            >>> instance = AcceptValidHeader('text/html;q=0.5, text/*')
            >>> instance.quality('text/html')
            1.0
        """

class _AcceptInvalidOrNoHeader(Accept):
    """
    Represent when an ``Accept`` header is invalid or not in request.

    This is the base class for the behaviour that :class:`.AcceptInvalidHeader`
    and :class:`.AcceptNoHeader` have in common.

    :rfc:`7231` does not provide any guidance on what should happen if the
    ``Accept`` header has an invalid value. This implementation disregards the
    header when the header is invalid, so :class:`.AcceptInvalidHeader` and
    :class:`.AcceptNoHeader` have much behaviour in common.
    """

    def __bool__(self) -> Literal[False]:
        """
        Return whether ``self`` represents a valid ``Accept`` header.

        Return ``True`` if ``self`` represents a valid header, and ``False`` if
        it represents an invalid header, or the header not being in the
        request.

        For this class, it always returns ``False``.
        """

    def __contains__(self, offer: str) -> Literal[True]:
        """
        Return ``bool`` indicating whether `offer` is acceptable.

        .. warning::

           The behavior of ``.__contains__`` for the ``Accept`` classes is
           currently being maintained for backward compatibility, but it will
           change in the future to better conform to the RFC.

        :param offer: (``str``) media type offer
        :return: (``bool``) Whether ``offer`` is acceptable according to the
                 header.

        For this class, either there is no ``Accept`` header in the request, or
        the header is invalid, so any media type is acceptable, and this always
        returns ``True``.
        """

    def __iter__(self) -> Iterator[str]:
        """
        Return all the ranges with non-0 qvalues, in order of preference.

        .. warning::

           The behavior of this method is currently maintained for backward
           compatibility, but will change in the future.

        :return: iterator of all the media ranges in the header with non-0
                 qvalues, in descending order of qvalue. If two ranges have the
                 same qvalue, they are returned in the order of their positions
                 in the header, from left to right.

        When there is no ``Accept`` header in the request or the header is
        invalid, there are no media ranges, so this always returns an empty
        iterator.
        """

    def accept_html(self) -> bool:
        """
        Return ``True`` if any HTML-like type is accepted.

        The HTML-like types are 'text/html', 'application/xhtml+xml',
        'application/xml' and 'text/xml'.

        When the header is invalid, or there is no `Accept` header in the
        request, all `offers` are considered acceptable, so this always returns
        ``True``.
        """

    @property
    def accepts_html(self) -> bool:
        """
        Return ``True`` if any HTML-like type is accepted.

        The HTML-like types are 'text/html', 'application/xhtml+xml',
        'application/xml' and 'text/xml'.

        When the header is invalid, or there is no `Accept` header in the
        request, all `offers` are considered acceptable, so this always returns
        ``True``.
        """

    def acceptable_offers(self, offers: Sequence[str]) -> list[tuple[str, float]]:
        """
        Return the offers that are acceptable according to the header.

        Any offers that cannot be parsed via
        :meth:`.Accept.parse_offer` will be ignored.

        :param offers: ``iterable`` of ``str`` media types (media types can
                       include media type parameters)
        :return: When the header is invalid, or there is no ``Accept`` header
                 in the request, all `offers` are considered acceptable, so
                 this method returns a list of (media type, qvalue) tuples
                 where each offer in `offers` is paired with the qvalue of 1.0,
                 in the same order as in `offers`.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: None = None) -> str | None:
        """
        Return the best match from the sequence of language tag `offers`.

        This is the ``.best_match()`` method for when the header is invalid or
        not found in the request, corresponding to
        :meth:`AcceptValidHeader.best_match`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future (see the documentation for
           :meth:`AcceptValidHeader.best_match`).

        When the header is invalid, or there is no `Accept` header in the
        request, all `offers` are considered acceptable, so the best match is
        the media type in `offers` with the highest server quality value (if
        the server quality value is not supplied for a media type, it is 1).

        If more than one media type in `offers` have the same highest server
        quality value, then the one that shows up first in `offers` is the best
        match.

        :param offers: (iterable)

                       | Each item in the iterable may be a ``str`` media type,
                         or a (media type, server quality value) ``tuple`` or
                         ``list``. (The two may be mixed in the iterable.)

        :param default_match: (optional, any type) the value to be returned if
                              `offers` is empty.

        :return: (``str``, or the type of `default_match`)

                 | The offer that has the highest server quality value.  If
                   `offers` is empty, the value of `default_match` is returned.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: str) -> str: ...
    def quality(self, offer: str) -> float:
        """
        Return quality value of given offer, or ``None`` if there is no match.

        This is the ``.quality()`` method for when the header is invalid or not
        found in the request, corresponding to
        :meth:`AcceptValidHeader.quality`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future (see the documentation for
           :meth:`AcceptValidHeader.quality`).

        :param offer: (``str``) media type offer
        :return: (``float``) ``1.0``.

        When the ``Accept`` header is invalid or not in the request, all offers
        are equally acceptable, so 1.0 is always returned.
        """

class AcceptNoHeader(_AcceptInvalidOrNoHeader):
    """
    Represent when there is no ``Accept`` header in the request.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptNoHeader.__add__`).
    """

    @property
    def header_value(self) -> None:
        """
        (``str`` or ``None``) The header value.

        As there is no header in the request, this is ``None``.
        """

    @property
    def parsed(self) -> None:
        """
        (``list`` or ``None``) Parsed form of the header.

        As there is no header in the request, this is ``None``.
        """

    def __init__(self) -> None:
        """
        Create an :class:`AcceptNoHeader` instance.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @overload
    def __add__(self, other: AcceptValidHeader | Literal[""]) -> AcceptValidHeader:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, with media ranges ``str``'s (including any media type
          parameters) as keys, and either qvalues ``float``'s or (*qvalues*,
          *extension_params*) tuples as values, where *extension_params* is a
          ``str`` of the extension parameters segment of the header element,
          starting with the first '``;``'
        * a ``tuple`` or ``list``, where each item is either a header element
          ``str``, or a (*media_range*, *qvalue*, *extension_params*) ``tuple``
          or ``list`` where *media_range* is a ``str`` of the media range
          including any media type parameters, and *extension_params* is a
          ``str`` of the extension parameters segment of the header element,
          starting with the first '``;``'
        * an :class:`AcceptValidHeader`, :class:`AcceptNoHeader`, or
          :class:`AcceptInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or an :class:`AcceptValidHeader`
        instance, a new :class:`AcceptValidHeader` instance with the valid
        header value is returned.

        If `other` is ``None``, an :class:`AcceptNoHeader` instance, an invalid
        header value, or an :class:`AcceptInvalidHeader` instance, a new
        :class:`AcceptNoHeader` instance is returned.
        """

    @overload
    def __add__(self, other: AcceptNoHeader | AcceptInvalidHeader | None) -> Self: ...
    @overload
    def __add__(
        self,
        other: (
            _AnyAcceptHeader
            | SupportsItems[str, float | tuple[float, str]]
            | _ListOrTuple[str | tuple[str, float, str] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self | AcceptValidHeader: ...
    @overload
    def __radd__(self, other: AcceptValidHeader | Literal[""]) -> AcceptValidHeader:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptNoHeader.__add__`.
        """

    @overload
    def __radd__(self, other: AcceptNoHeader | AcceptInvalidHeader | None) -> Self: ...
    @overload
    def __radd__(
        self,
        other: (
            _AnyAcceptHeader
            | SupportsItems[str, float | tuple[float, str]]
            | _ListOrTuple[str | tuple[str, float, str] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self | AcceptValidHeader: ...

class AcceptInvalidHeader(_AcceptInvalidOrNoHeader):
    """
    Represent an invalid ``Accept`` header.

    An invalid header is one that does not conform to
    :rfc:`7231#section-5.3.2`.

    :rfc:`7231` does not provide any guidance on what should happen if the
    ``Accept`` header has an invalid value. This implementation disregards the
    header, and treats it as if there is no ``Accept`` header in the request.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptInvalidHeader.__add__`).
    """

    @property
    def header_value(self) -> str:
        """(``str`` or ``None``) The header value."""

    @property
    def parsed(self) -> None:
        """
        (``list`` or ``None``) Parsed form of the header.

        As the header is invalid and cannot be parsed, this is ``None``.
        """

    def __init__(self, header_value: str) -> None:
        """
        Create an :class:`AcceptInvalidHeader` instance.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @overload
    def __add__(self, other: AcceptValidHeader | Literal[""]) -> AcceptValidHeader:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, with media ranges ``str``'s (including any media type
          parameters) as keys, and either qvalues ``float``'s or (*qvalues*,
          *extension_params*) tuples as values, where *extension_params* is a
          ``str`` of the extension parameters segment of the header element,
          starting with the first '``;``'
        * a ``tuple`` or ``list``, where each item is either a header element
          ``str``, or a (*media_range*, *qvalue*, *extension_params*) ``tuple``
          or ``list`` where *media_range* is a ``str`` of the media range
          including any media type parameters, and *extension_params* is a
          ``str`` of the extension parameters segment of the header element,
          starting with the first '``;``'
        * an :class:`AcceptValidHeader`, :class:`AcceptNoHeader`, or
          :class:`AcceptInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or an :class:`AcceptValidHeader`
        instance, then a new :class:`AcceptValidHeader` instance with the valid
        header value is returned.

        If `other` is ``None``, an :class:`AcceptNoHeader` instance, an invalid
        header value, or an :class:`AcceptInvalidHeader` instance, a new
        :class:`AcceptNoHeader` instance is returned.
        """

    @overload
    def __add__(self, other: AcceptInvalidHeader | AcceptNoHeader | None) -> AcceptNoHeader: ...
    @overload
    def __add__(
        self,
        other: (
            _AnyAcceptHeader
            | SupportsItems[str, float | tuple[float, str]]
            | _ListOrTuple[str | tuple[str, float, str] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> AcceptValidHeader | AcceptNoHeader: ...
    @overload
    def __radd__(self, other: AcceptValidHeader | Literal[""]) -> AcceptValidHeader:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptValidHeader.__add__`.
        """

    @overload
    def __radd__(self, other: AcceptInvalidHeader | AcceptNoHeader | None) -> AcceptNoHeader: ...
    @overload
    def __radd__(
        self,
        other: (
            _AnyAcceptHeader
            | SupportsItems[str, float | tuple[float, str]]
            | _ListOrTuple[str | tuple[str, float, str] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> AcceptValidHeader | AcceptNoHeader: ...

@overload
def create_accept_header(header_value: AcceptValidHeader | Literal[""]) -> AcceptValidHeader:
    """
    Create an object representing the ``Accept`` header in a request.

    :param header_value: (``str``) header value
    :return: If `header_value` is ``None``, an :class:`AcceptNoHeader`
             instance.

             | If `header_value` is a valid ``Accept`` header, an
               :class:`AcceptValidHeader` instance.

             | If `header_value` is an invalid ``Accept`` header, an
               :class:`AcceptInvalidHeader` instance.
    """

@overload
def create_accept_header(header_value: AcceptInvalidHeader) -> AcceptInvalidHeader: ...
@overload
def create_accept_header(header_value: None | AcceptNoHeader) -> AcceptNoHeader: ...
@overload
def create_accept_header(header_value: str) -> AcceptValidHeader | AcceptInvalidHeader: ...
@overload
def create_accept_header(header_value: _AnyAcceptHeader | str | None) -> _AnyAcceptHeader: ...
def accept_property() -> _AcceptProperty: ...

class AcceptCharset:
    """
    Represent an ``Accept-Charset`` header.

    Base class for :class:`AcceptCharsetValidHeader`,
    :class:`AcceptCharsetNoHeader`, and :class:`AcceptCharsetInvalidHeader`.
    """

    @classmethod
    def parse(cls, value: str) -> Iterator[tuple[str, float]]:
        """
        Parse an ``Accept-Charset`` header.

        :param value: (``str``) header value
        :return: If `value` is a valid ``Accept-Charset`` header, returns an
                 iterator of (charset, quality value) tuples, as parsed from
                 the header from left to right.
        :raises ValueError: if `value` is an invalid header
        """

class AcceptCharsetValidHeader(AcceptCharset):
    """
    Represent a valid ``Accept-Charset`` header.

    A valid header is one that conforms to :rfc:`RFC 7231, section 5.3.3
    <7231#section-5.3.3>`.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptCharsetValidHeader.__add__`).
    """

    @property
    def header_value(self) -> str:
        """(``str``) The header value."""

    @property
    def parsed(self) -> list[tuple[str, float]]:
        """
        (``list``) Parsed form of the header.

        A list of (charset, quality value) tuples.
        """

    def __init__(self, header_value: str) -> None:
        """
        Create an :class:`AcceptCharsetValidHeader` instance.

        :param header_value: (``str``) header value.
        :raises ValueError: if `header_value` is an invalid value for an
                            ``Accept-Charset`` header.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    def __add__(
        self,
        other: (
            _AnyAcceptCharsetHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, where keys are charsets and values are qvalues
        * a ``tuple`` or ``list``, where each item is a charset ``str`` or a
          ``tuple`` or ``list`` (charset, qvalue) pair (``str``'s and pairs
          can be mixed within the ``tuple`` or ``list``)
        * an :class:`AcceptCharsetValidHeader`, :class:`AcceptCharsetNoHeader`,
          or :class:`AcceptCharsetInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or another
        :class:`AcceptCharsetValidHeader` instance, the two header values are
        joined with ``', '``, and a new :class:`AcceptCharsetValidHeader`
        instance with the new header value is returned.

        If `other` is ``None``, an :class:`AcceptCharsetNoHeader` instance, an
        invalid header value, or an :class:`AcceptCharsetInvalidHeader`
        instance, a new :class:`AcceptCharsetValidHeader` instance with the
        same header value as ``self`` is returned.
        """

    def __bool__(self) -> Literal[True]:
        """
        Return whether ``self`` represents a valid ``Accept-Charset`` header.

        Return ``True`` if ``self`` represents a valid header, and ``False`` if
        it represents an invalid header, or the header not being in the
        request.

        For this class, it always returns ``True``.
        """

    def __contains__(self, offer: str) -> bool:
        """
        Return ``bool`` indicating whether `offer` is acceptable.

        .. warning::

           The behavior of :meth:`AcceptCharsetValidHeader.__contains__` is
           currently being maintained for backward compatibility, but it will
           change in the future to better conform to the RFC.

        :param offer: (``str``) charset offer
        :return: (``bool``) Whether ``offer`` is acceptable according to the
                 header.

        This does not fully conform to :rfc:`RFC 7231, section 5.3.3
        <7231#section-5.3.3>`: it incorrect interprets ``*`` to mean 'match any
        charset in the header', rather than 'match any charset that is not
        mentioned elsewhere in the header'::

            >>> 'UTF-8' in AcceptCharsetValidHeader('UTF-8;q=0, *')
            True
        """

    def __iter__(self) -> Iterator[str]:
        """
        Return all the items with non-0 qvalues, in order of preference.

        .. warning::

           The behavior of this method is currently maintained for backward
           compatibility, but will change in the future.

        :return: iterator of all the items (charset or ``*``) in the header
                 with non-0 qvalues, in descending order of qvalue. If two
                 items have the same qvalue, they are returned in the order of
                 their positions in the header, from left to right.

        Please note that this is a simple filter for the items in the header
        with non-0 qvalues, and is not necessarily the same as what the client
        prefers, e.g. ``'utf-7;q=0, *'`` means 'everything but utf-7', but
        ``list(instance)`` would return only ``['*']``.
        """

    def __radd__(
        self,
        other: (
            _AnyAcceptCharsetHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptCharsetValidHeader.__add__`.
        """

    def acceptable_offers(self, offers: Sequence[str]) -> list[tuple[str, float]]:
        """
        Return the offers that are acceptable according to the header.

        The offers are returned in descending order of preference, where
        preference is indicated by the qvalue of the charset or ``*`` in the
        header matching the offer.

        This uses the matching rules described in :rfc:`RFC 7231, section 5.3.3
        <7231#section-5.3.3>`.

        :param offers: ``iterable`` of ``str`` charsets
        :return: A list of tuples of the form (charset, qvalue), in descending
                 order of qvalue. Where two offers have the same qvalue, they
                 are returned in the same order as their order in `offers`.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: None = None) -> str | None:
        """
        Return the best match from the sequence of charset `offers`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future.

           :meth:`AcceptCharsetValidHeader.best_match`  has many issues, and
           does not conform to :rfc:`RFC 7231 <7231>`.

        Each charset in `offers` is checked against each non-``q=0`` item
        (charset or ``*``) in the header. If the two are a match according to
        WebOb's old criterion for a match, the quality value of the match is
        the qvalue of the item from the header multiplied by the server quality
        value of the offer (if the server quality value is not supplied, it is
        1).

        The offer in the match with the highest quality value is the best
        match. If there is more than one match with the highest qvalue, the one
        that shows up first in `offers` is the best match.

        :param offers: (iterable)

                       | Each item in the iterable may be a ``str`` charset, or
                         a (charset, server quality value) ``tuple`` or
                         ``list``.  (The two may be mixed in the iterable.)

        :param default_match: (optional, any type) the value to be returned if
                              there is no match

        :return: (``str``, or the type of `default_match`)

                 | The offer that is the best match. If there is no match, the
                   value of `default_match` is returned.

        The algorithm behind this method was written for the ``Accept`` header
        rather than the ``Accept-Charset`` header. It uses the old criterion of
        a match in :meth:`AcceptCharsetValidHeader._old_match`, which does not
        conform to :rfc:`RFC 7231, section 5.3.3 <7231#section-5.3.3>`, in that
        it does not interpret ``*`` values in the header correctly: ``*``
        should only match charsets not mentioned elsewhere in the header::

            >>> AcceptCharsetValidHeader('utf-8;q=0, *').best_match(['utf-8'])
            'utf-8'
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: str) -> str: ...
    def quality(self, offer: str) -> float | None:
        """
        Return quality value of given offer, or ``None`` if there is no match.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future.

        :param offer: (``str``) charset offer
        :return: (``float`` or ``None``)

                 | The quality value from the charset that matches the `offer`,
                   or ``None`` if there is no match.

        This uses the old criterion of a match in
        :meth:`AcceptCharsetValidHeader._old_match`, which does not conform to
        :rfc:`RFC 7231, section 5.3.3 <7231#section-5.3.3>`, in that it does
        not interpret ``*`` values in the header correctly: ``*`` should only
        match charsets not mentioned elsewhere in the header::

            >>> AcceptCharsetValidHeader('utf-8;q=0, *').quality('utf-8')
            1.0
            >>> AcceptCharsetValidHeader('utf-8;q=0.9, *').quality('utf-8')
            1.0
        """

class _AcceptCharsetInvalidOrNoHeader(AcceptCharset):
    """
    Represent when an ``Accept-Charset`` header is invalid or not in request.

    This is the base class for the behaviour that
    :class:`.AcceptCharsetInvalidHeader` and :class:`.AcceptCharsetNoHeader`
    have in common.

    :rfc:`7231` does not provide any guidance on what should happen if the
    ``Accept-Charset`` header has an invalid value. This implementation
    disregards the header when the header is invalid, so
    :class:`.AcceptCharsetInvalidHeader` and :class:`.AcceptCharsetNoHeader`
    have much behaviour in common.
    """

    def __bool__(self) -> Literal[False]:
        """
        Return whether ``self`` represents a valid ``Accept-Charset`` header.

        Return ``True`` if ``self`` represents a valid header, and ``False`` if
        it represents an invalid header, or the header not being in the
        request.

        For this class, it always returns ``False``.
        """

    def __contains__(self, offer: str) -> Literal[True]:
        """
        Return ``bool`` indicating whether `offer` is acceptable.

        .. warning::

           The behavior of ``.__contains__`` for the ``AcceptCharset`` classes
           is currently being maintained for backward compatibility, but it
           will change in the future to better conform to the RFC.

        :param offer: (``str``) charset offer
        :return: (``bool``) Whether ``offer`` is acceptable according to the
                 header.

        For this class, either there is no ``Accept-Charset`` header in the
        request, or the header is invalid, so any charset is acceptable, and
        this always returns ``True``.
        """

    def __iter__(self) -> Iterator[str]:
        """
        Return all the items with non-0 qvalues, in order of preference.

        .. warning::

           The behavior of this method is currently maintained for backward
           compatibility, but will change in the future.

        :return: iterator of all the items (charset or ``*``) in the header
                 with non-0 qvalues, in descending order of qvalue. If two
                 items have the same qvalue, they are returned in the order of
                 their positions in the header, from left to right.

        When there is no ``Accept-Charset`` header in the request or the header
        is invalid, there are no items, and this always returns an empty
        iterator.
        """

    def acceptable_offers(self, offers: Iterable[str]) -> list[tuple[str, float]]:
        """
        Return the offers that are acceptable according to the header.

        The offers are returned in descending order of preference, where
        preference is indicated by the qvalue of the charset or ``*`` in the
        header matching the offer.

        This uses the matching rules described in :rfc:`RFC 7231, section 5.3.3
        <7231#section-5.3.3>`.

        :param offers: ``iterable`` of ``str`` charsets
        :return: A list of tuples of the form (charset, qvalue), in descending
                 order of qvalue. Where two offers have the same qvalue, they
                 are returned in the same order as their order in `offers`.

                 | When the header is invalid or there is no ``Accept-Charset``
                   header in the request, all `offers` are considered
                   acceptable, so this method returns a list of (charset,
                   qvalue) tuples where each offer in `offers` is paired with
                   the qvalue of 1.0, in the same order as `offers`.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: None = None) -> str | None:
        """
        Return the best match from the sequence of charset `offers`.

        This is the ``.best_match()`` method for when the header is invalid or
        not found in the request, corresponding to
        :meth:`AcceptCharsetValidHeader.best_match`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future (see the documentation for
           :meth:`AcceptCharsetValidHeader.best_match`).

        When the header is invalid, or there is no `Accept-Charset` header in
        the request, all the charsets in `offers` are considered acceptable, so
        the best match is the charset in `offers` with the highest server
        quality value (if the server quality value is not supplied, it is 1).

        If more than one charsets in `offers` have the same highest server
        quality value, then the one that shows up first in `offers` is the best
        match.

        :param offers: (iterable)

                       | Each item in the iterable may be a ``str`` charset, or
                         a (charset, server quality value) ``tuple`` or
                         ``list``.  (The two may be mixed in the iterable.)

        :param default_match: (optional, any type) the value to be returned if
                              `offers` is empty.

        :return: (``str``, or the type of `default_match`)

                 | The charset that has the highest server quality value.  If
                   `offers` is empty, the value of `default_match` is returned.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: str) -> str: ...
    def quality(self, offer: str) -> float | None:
        """
        Return quality value of given offer, or ``None`` if there is no match.

        This is the ``.quality()`` method for when the header is invalid or not
        found in the request, corresponding to
        :meth:`AcceptCharsetValidHeader.quality`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future (see the documentation for
           :meth:`AcceptCharsetValidHeader.quality`).

        :param offer: (``str``) charset offer
        :return: (``float``) ``1.0``.

        When the ``Accept-Charset`` header is invalid or not in the request,
        all offers are equally acceptable, so 1.0 is always returned.
        """

class AcceptCharsetNoHeader(_AcceptCharsetInvalidOrNoHeader):
    """
    Represent when there is no ``Accept-Charset`` header in the request.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptCharsetNoHeader.__add__`).
    """

    @property
    def header_value(self) -> None:
        """
        (``str`` or ``None``) The header value.

        As there is no header in the request, this is ``None``.
        """

    @property
    def parsed(self) -> None:
        """
        (``list`` or ``None``) Parsed form of the header.

        As there is no header in the request, this is ``None``.
        """

    def __init__(self) -> None:
        """
        Create an :class:`AcceptCharsetNoHeader` instance.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @overload
    def __add__(self, other: AcceptCharsetValidHeader) -> AcceptCharsetValidHeader:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, where keys are charsets and values are qvalues
        * a ``tuple`` or ``list``, where each item is a charset ``str`` or a
          ``tuple`` or ``list`` (charset, qvalue) pair (``str``'s and pairs
          can be mixed within the ``tuple`` or ``list``)
        * an :class:`AcceptCharsetValidHeader`, :class:`AcceptCharsetNoHeader`,
          or :class:`AcceptCharsetInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or an
        :class:`AcceptCharsetValidHeader` instance, a new
        :class:`AcceptCharsetValidHeader` instance with the valid header value
        is returned.

        If `other` is ``None``, an :class:`AcceptCharsetNoHeader` instance, an
        invalid header value, or an :class:`AcceptCharsetInvalidHeader`
        instance, a new :class:`AcceptCharsetNoHeader` instance is returned.
        """

    @overload
    def __add__(self, other: AcceptCharsetInvalidHeader | AcceptCharsetNoHeader | Literal[""] | None) -> Self: ...
    @overload
    def __add__(
        self,
        other: (
            _AnyAcceptCharsetHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self | AcceptCharsetValidHeader: ...
    @overload
    def __radd__(self, other: AcceptCharsetValidHeader) -> AcceptCharsetValidHeader:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptCharsetNoHeader.__add__`.
        """

    @overload
    def __radd__(self, other: AcceptCharsetInvalidHeader | AcceptCharsetNoHeader | Literal[""] | None) -> Self: ...
    @overload
    def __radd__(
        self,
        other: (
            _AnyAcceptCharsetHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self | AcceptCharsetValidHeader: ...

class AcceptCharsetInvalidHeader(_AcceptCharsetInvalidOrNoHeader):
    """
    Represent an invalid ``Accept-Charset`` header.

    An invalid header is one that does not conform to
    :rfc:`7231#section-5.3.3`. As specified in the RFC, an empty header is an
    invalid ``Accept-Charset`` header.

    :rfc:`7231` does not provide any guidance on what should happen if the
    ``Accept-Charset`` header has an invalid value. This implementation
    disregards the header, and treats it as if there is no ``Accept-Charset``
    header in the request.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptCharsetInvalidHeader.__add__`).
    """

    @property
    def header_value(self) -> str:
        """(``str`` or ``None``) The header value."""

    @property
    def parsed(self) -> None:
        """
        (``list`` or ``None``) Parsed form of the header.

        As the header is invalid and cannot be parsed, this is ``None``.
        """

    def __init__(self, header_value: str) -> None:
        """
        Create an :class:`AcceptCharsetInvalidHeader` instance.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @overload
    def __add__(self, other: AcceptCharsetValidHeader) -> AcceptCharsetValidHeader:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, where keys are charsets and values are qvalues
        * a ``tuple`` or ``list``, where each item is a charset ``str`` or a
          ``tuple`` or ``list`` (charset, qvalue) pair (``str``'s and pairs
          can be mixed within the ``tuple`` or ``list``)
        * an :class:`AcceptCharsetValidHeader`, :class:`AcceptCharsetNoHeader`,
          or :class:`AcceptCharsetInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or an
        :class:`AcceptCharsetValidHeader` instance, a new
        :class:`AcceptCharsetValidHeader` instance with the valid header value
        is returned.

        If `other` is ``None``, an :class:`AcceptCharsetNoHeader` instance, an
        invalid header value, or an :class:`AcceptCharsetInvalidHeader`
        instance, a new :class:`AcceptCharsetNoHeader` instance is returned.
        """

    @overload
    def __add__(
        self, other: AcceptCharsetInvalidHeader | AcceptCharsetNoHeader | Literal[""] | None
    ) -> AcceptCharsetNoHeader: ...
    @overload
    def __add__(
        self,
        other: (
            _AnyAcceptCharsetHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> AcceptCharsetValidHeader | AcceptCharsetNoHeader: ...
    @overload
    def __radd__(self, other: AcceptCharsetValidHeader) -> AcceptCharsetValidHeader:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptCharsetValidHeader.__add__`.
        """

    @overload
    def __radd__(
        self, other: AcceptCharsetInvalidHeader | AcceptCharsetNoHeader | Literal[""] | None
    ) -> AcceptCharsetNoHeader: ...
    @overload
    def __radd__(
        self,
        other: (
            _AnyAcceptCharsetHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> AcceptCharsetValidHeader | AcceptCharsetNoHeader: ...

@overload
def create_accept_charset_header(header_value: AcceptCharsetValidHeader | Literal[""]) -> AcceptCharsetValidHeader:
    """
    Create an object representing the ``Accept-Charset`` header in a request.

    :param header_value: (``str``) header value
    :return: If `header_value` is ``None``, an :class:`AcceptCharsetNoHeader`
             instance.

             | If `header_value` is a valid ``Accept-Charset`` header, an
               :class:`AcceptCharsetValidHeader` instance.

             | If `header_value` is an invalid ``Accept-Charset`` header, an
               :class:`AcceptCharsetInvalidHeader` instance.
    """

@overload
def create_accept_charset_header(header_value: AcceptCharsetInvalidHeader) -> AcceptCharsetInvalidHeader: ...
@overload
def create_accept_charset_header(header_value: AcceptCharsetNoHeader | None) -> AcceptCharsetNoHeader: ...
@overload
def create_accept_charset_header(header_value: str) -> AcceptCharsetValidHeader | AcceptCharsetInvalidHeader: ...
@overload
def create_accept_charset_header(header_value: _AnyAcceptCharsetHeader | str | None) -> _AnyAcceptCharsetHeader: ...
def accept_charset_property() -> _AcceptCharsetProperty: ...

class AcceptEncoding:
    """
    Represent an ``Accept-Encoding`` header.

    Base class for :class:`AcceptEncodingValidHeader`,
    :class:`AcceptEncodingNoHeader`, and :class:`AcceptEncodingInvalidHeader`.
    """

    @classmethod
    def parse(cls, value: str) -> Iterator[tuple[str, float]]:
        """
        Parse an ``Accept-Encoding`` header.

        :param value: (``str``) header value
        :return: If `value` is a valid ``Accept-Encoding`` header, returns an
                 iterator of (codings, quality value) tuples, as parsed from
                 the header from left to right.
        :raises ValueError: if `value` is an invalid header
        """

class AcceptEncodingValidHeader(AcceptEncoding):
    """
    Represent a valid ``Accept-Encoding`` header.

    A valid header is one that conforms to :rfc:`RFC 7231, section 5.3.4
    <7231#section-5.3.4>`.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptEncodingValidHeader.__add__`).
    """

    @property
    def header_value(self) -> str:
        """(``str`` or ``None``) The header value."""

    @property
    def parsed(self) -> list[tuple[str, float]]:
        """
        (``list`` or ``None``) Parsed form of the header.

        A list of (*codings*, *qvalue*) tuples, where

        *codings* (``str``) is a content-coding, the string "``identity``", or
        "``*``"; and

        *qvalue* (``float``) is the quality value of the codings.
        """

    def __init__(self, header_value: str) -> None:
        """
        Create an :class:`AcceptEncodingValidHeader` instance.

        :param header_value: (``str``) header value.
        :raises ValueError: if `header_value` is an invalid value for an
                            ``Accept-Encoding`` header.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    def __add__(
        self,
        other: (
            _AnyAcceptEncodingHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, with content-coding, ``identity`` or ``*`` ``str``'s as
          keys, and qvalue ``float``'s as values
        * a ``tuple`` or ``list``, where each item is either a header element
          ``str``, or a (content-coding/``identity``/``*``, qvalue) ``tuple``
          or ``list``
        * an :class:`AcceptEncodingValidHeader`,
          :class:`AcceptEncodingNoHeader`, or
          :class:`AcceptEncodingInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or another
        :class:`AcceptEncodingValidHeader` instance, and the header value it
        represents is not ``''``, then the two header values are joined with
        ``', '``, and a new :class:`AcceptEncodingValidHeader` instance with
        the new header value is returned.

        If `other` is a valid header value or another
        :class:`AcceptEncodingValidHeader` instance representing a header value
        of ``''``; or if it is ``None`` or an :class:`AcceptEncodingNoHeader`
        instance; or if it is an invalid header value, or an
        :class:`AcceptEncodingInvalidHeader` instance, then a new
        :class:`AcceptEncodingValidHeader` instance with the same header value
        as ``self`` is returned.
        """

    def __bool__(self) -> Literal[True]:
        """
        Return whether ``self`` represents a valid ``Accept-Encoding`` header.

        Return ``True`` if ``self`` represents a valid header, and ``False`` if
        it represents an invalid header, or the header not being in the
        request.

        For this class, it always returns ``True``.
        """

    def __contains__(self, offer: str) -> bool:
        """
        Return ``bool`` indicating whether `offer` is acceptable.

        .. warning::

           The behavior of :meth:`AcceptEncodingValidHeader.__contains__` is
           currently being maintained for backward compatibility, but it will
           change in the future to better conform to the RFC.

        :param offer: (``str``) a content-coding or ``identity`` offer
        :return: (``bool``) Whether ``offer`` is acceptable according to the
                 header.

        The behavior of this method does not fully conform to :rfc:`7231`.
        It does not correctly interpret ``*``::

            >>> 'gzip' in AcceptEncodingValidHeader('gzip;q=0, *')
            True

        and does not handle the ``identity`` token correctly::

            >>> 'identity' in AcceptEncodingValidHeader('gzip')
            False
        """

    def __iter__(self) -> Iterator[str]:
        """
        Return all the ranges with non-0 qvalues, in order of preference.

        .. warning::

           The behavior of this method is currently maintained for backward
           compatibility, but will change in the future.

        :return: iterator of all the (content-coding/``identity``/``*``) items
                 in the header with non-0 qvalues, in descending order of
                 qvalue. If two items have the same qvalue, they are returned
                 in the order of their positions in the header, from left to
                 right.

        Please note that this is a simple filter for the items in the header
        with non-0 qvalues, and is not necessarily the same as what the client
        prefers, e.g. ``'gzip;q=0, *'`` means 'everything but gzip', but
        ``list(instance)`` would return only ``['*']``.
        """

    def __radd__(
        self,
        other: (
            _AnyAcceptEncodingHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptEncodingValidHeader.__add__`.
        """

    def acceptable_offers(self, offers: Sequence[str]) -> list[tuple[str, float]]:
        """
        Return the offers that are acceptable according to the header.

        The offers are returned in descending order of preference, where
        preference is indicated by the qvalue of the item (content-coding,
        "identity" or "*") in the header that matches the offer.

        This uses the matching rules described in :rfc:`RFC 7231, section 5.3.4
        <7231#section-5.3.4>`.

        :param offers: ``iterable`` of ``str``s, where each ``str`` is a
                       content-coding or the string ``identity`` (the token
                       used to represent "no encoding")
        :return: A list of tuples of the form (content-coding or "identity",
                 qvalue), in descending order of qvalue. Where two offers have
                 the same qvalue, they are returned in the same order as their
                 order in `offers`.

        Use the string ``'identity'`` (without the quotes) in `offers` to
        indicate an offer with no content-coding. From the RFC: 'If the
        representation has no content-coding, then it is acceptable by default
        unless specifically excluded by the Accept-Encoding field stating
        either "identity;q=0" or "\\*;q=0" without a more specific entry for
        "identity".' The RFC does not specify the qvalue that should be
        assigned to the representation/offer with no content-coding; this
        implementation assigns it a qvalue of 1.0.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: None = None) -> str | None:
        """
        Return the best match from the sequence of `offers`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future.

           :meth:`AcceptEncodingValidHeader.best_match` uses its own algorithm
           (one not specified in :rfc:`RFC 7231 <7231>`) to determine what is a
           best match. The algorithm has many issues, and does not conform to
           the RFC.

        Each offer in `offers` is checked against each non-``q=0`` item
        (content-coding/``identity``/``*``) in the header. If the two are a
        match according to WebOb's old criterion for a match, the quality value
        of the match is the qvalue of the item from the header multiplied by
        the server quality value of the offer (if the server quality value is
        not supplied, it is 1).

        The offer in the match with the highest quality value is the best
        match. If there is more than one match with the highest qvalue, the one
        that shows up first in `offers` is the best match.

        :param offers: (iterable)

                       | Each item in the iterable may be a ``str`` *codings*,
                         or a (*codings*, server quality value) ``tuple`` or
                         ``list``, where *codings* is either a content-coding,
                         or the string ``identity`` (which represents *no
                         encoding*). ``str`` and ``tuple``/``list`` elements
                         may be mixed within the iterable.

        :param default_match: (optional, any type) the value to be returned if
                              there is no match

        :return: (``str``, or the type of `default_match`)

                 | The offer that is the best match. If there is no match, the
                   value of `default_match` is returned.

        This method does not conform to :rfc:`RFC 7231, section 5.3.4
        <7231#section-5.3.4>`, in that it does not correctly interpret ``*``::

            >>> AcceptEncodingValidHeader('gzip;q=0, *').best_match(['gzip'])
            'gzip'

        and does not handle the ``identity`` token correctly::

            >>> instance = AcceptEncodingValidHeader('gzip')
            >>> instance.best_match(['identity']) is None
            True
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: str) -> str: ...
    def quality(self, offer: str) -> float | None:
        """
        Return quality value of given offer, or ``None`` if there is no match.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future.

        :param offer: (``str``) A content-coding, or ``identity``.
        :return: (``float`` or ``None``)

                 | The quality value from the header item
                   (content-coding/``identity``/``*``) that matches the
                   `offer`, or ``None`` if there is no match.

        The behavior of this method does not conform to :rfc:`RFC 7231, section
        5.3.4<7231#section-5.3.4>`, in that it does not correctly interpret
        ``*``::

            >>> AcceptEncodingValidHeader('gzip;q=0, *').quality('gzip')
            1.0

        and does not handle the ``identity`` token correctly::

            >>> AcceptEncodingValidHeader('gzip').quality('identity') is None
            True
        """

class _AcceptEncodingInvalidOrNoHeader(AcceptEncoding):
    """
    Represent when an ``Accept-Encoding`` header is invalid or not in request.

    This is the base class for the behaviour that
    :class:`.AcceptEncodingInvalidHeader` and :class:`.AcceptEncodingNoHeader`
    have in common.

    :rfc:`7231` does not provide any guidance on what should happen if the
    ``AcceptEncoding`` header has an invalid value. This implementation
    disregards the header when the header is invalid, so
    :class:`.AcceptEncodingInvalidHeader` and :class:`.AcceptEncodingNoHeader`
    have much behaviour in common.
    """

    def __bool__(self) -> Literal[False]:
        """
        Return whether ``self`` represents a valid ``Accept-Encoding`` header.

        Return ``True`` if ``self`` represents a valid header, and ``False`` if
        it represents an invalid header, or the header not being in the
        request.

        For this class, it always returns ``False``.
        """

    def __contains__(self, offer: str) -> Literal[True]:
        """
        Return ``bool`` indicating whether `offer` is acceptable.

        .. warning::

           The behavior of ``.__contains__`` for the ``Accept-Encoding``
           classes is currently being maintained for backward compatibility,
           but it will change in the future to better conform to the RFC.

        :param offer: (``str``) a content-coding or ``identity`` offer
        :return: (``bool``) Whether ``offer`` is acceptable according to the
                 header.

        For this class, either there is no ``Accept-Encoding`` header in the
        request, or the header is invalid, so any content-coding is acceptable,
        and this always returns ``True``.
        """

    def __iter__(self) -> Iterator[str]:
        """
        Return all the header items with non-0 qvalues, in order of preference.

        .. warning::

           The behavior of this method is currently maintained for backward
           compatibility, but will change in the future.

        :return: iterator of all the (content-coding/``identity``/``*``) items
                 in the header with non-0 qvalues, in descending order of
                 qvalue. If two items have the same qvalue, they are returned
                 in the order of their positions in the header, from left to
                 right.

        When there is no ``Accept-Encoding`` header in the request or the
        header is invalid, there are no items in the header, so this always
        returns an empty iterator.
        """

    def acceptable_offers(self, offers: Iterable[str]) -> list[tuple[str, float]]:
        """
        Return the offers that are acceptable according to the header.

        :param offers: ``iterable`` of ``str``s, where each ``str`` is a
                       content-coding or the string ``identity`` (the token
                       used to represent "no encoding")
        :return: When the header is invalid, or there is no ``Accept-Encoding``
                 header in the request, all `offers` are considered acceptable,
                 so this method returns a list of (content-coding or
                 "identity", qvalue) tuples where each offer in `offers` is
                 paired with the qvalue of 1.0, in the same order as in
                 `offers`.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: None = None) -> str | None:
        """
        Return the best match from the sequence of `offers`.

        This is the ``.best_match()`` method for when the header is invalid or
        not found in the request, corresponding to
        :meth:`AcceptEncodingValidHeader.best_match`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future (see the documentation for
           :meth:`AcceptEncodingValidHeader.best_match`).

        When the header is invalid, or there is no `Accept-Encoding` header in
        the request, all `offers` are considered acceptable, so the best match
        is the offer in `offers` with the highest server quality value (if the
        server quality value is not supplied for a media type, it is 1).

        If more than one offer in `offers` have the same highest server quality
        value, then the one that shows up first in `offers` is the best match.

        :param offers: (iterable)

                       | Each item in the iterable may be a ``str`` *codings*,
                         or a (*codings*, server quality value) ``tuple`` or
                         ``list``, where *codings* is either a content-coding,
                         or the string ``identity`` (which represents *no
                         encoding*). ``str`` and ``tuple``/``list`` elements
                         may be mixed within the iterable.

        :param default_match: (optional, any type) the value to be returned if
                              `offers` is empty.

        :return: (``str``, or the type of `default_match`)

                 | The offer that has the highest server quality value. If
                   `offers` is empty, the value of `default_match` is returned.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: str) -> str: ...
    def quality(self, offer: str) -> float | None:
        """
        Return quality value of given offer, or ``None`` if there is no match.

        This is the ``.quality()`` method for when the header is invalid or not
        found in the request, corresponding to
        :meth:`AcceptEncodingValidHeader.quality`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future (see the documentation for
           :meth:`AcceptEncodingValidHeader.quality`).

        :param offer: (``str``) A content-coding, or ``identity``.
        :return: (``float``) ``1.0``.

        When the ``Accept-Encoding`` header is invalid or not in the request,
        all offers are equally acceptable, so 1.0 is always returned.
        """

class AcceptEncodingNoHeader(_AcceptEncodingInvalidOrNoHeader):
    """
    Represent when there is no ``Accept-Encoding`` header in the request.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptEncodingNoHeader.__add__`).
    """

    @property
    def header_value(self) -> None:
        """
        (``str`` or ``None``) The header value.

        As there is no header in the request, this is ``None``.
        """

    @property
    def parsed(self) -> None:
        """
        (``list`` or ``None``) Parsed form of the header.

        As there is no header in the request, this is ``None``.
        """

    def __init__(self) -> None:
        """
        Create an :class:`AcceptEncodingNoHeader` instance.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @overload
    def __add__(self, other: AcceptEncodingValidHeader | Literal[""]) -> AcceptEncodingValidHeader:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, with content-coding, ``identity`` or ``*`` ``str``'s as
          keys, and qvalue ``float``'s as values
        * a ``tuple`` or ``list``, where each item is either a header element
          ``str``, or a (content-coding/``identity``/``*``, qvalue) ``tuple``
          or ``list``
        * an :class:`AcceptEncodingValidHeader`,
          :class:`AcceptEncodingNoHeader`, or
          :class:`AcceptEncodingInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or an
        :class:`AcceptEncodingValidHeader` instance, a new
        :class:`AcceptEncodingValidHeader` instance with the valid header value
        is returned.

        If `other` is ``None``, an :class:`AcceptEncodingNoHeader` instance, an
        invalid header value, or an :class:`AcceptEncodingInvalidHeader`
        instance, a new :class:`AcceptEncodingNoHeader` instance is returned.
        """

    @overload
    def __add__(self, other: AcceptEncodingInvalidHeader | AcceptEncodingNoHeader | None) -> Self: ...
    @overload
    def __add__(
        self,
        other: (
            _AnyAcceptEncodingHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self | AcceptEncodingValidHeader: ...
    @overload
    def __radd__(self, other: AcceptEncodingValidHeader | Literal[""]) -> AcceptEncodingValidHeader:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptEncodingNoHeader.__add__`.
        """

    @overload
    def __radd__(self, other: AcceptEncodingInvalidHeader | AcceptEncodingNoHeader | None) -> Self: ...
    @overload
    def __radd__(
        self,
        other: (
            _AnyAcceptEncodingHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self | AcceptEncodingValidHeader: ...

class AcceptEncodingInvalidHeader(_AcceptEncodingInvalidOrNoHeader):
    """
    Represent an invalid ``Accept-Encoding`` header.

    An invalid header is one that does not conform to
    :rfc:`7231#section-5.3.4`.

    :rfc:`7231` does not provide any guidance on what should happen if the
    ``Accept-Encoding`` header has an invalid value. This implementation
    disregards the header, and treats it as if there is no ``Accept-Encoding``
    header in the request.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptEncodingInvalidHeader.__add__`).
    """

    @property
    def header_value(self) -> str:
        """(``str`` or ``None``) The header value."""

    @property
    def parsed(self) -> None:
        """
        (``list`` or ``None``) Parsed form of the header.

        As the header is invalid and cannot be parsed, this is ``None``.
        """

    def __init__(self, header_value: str) -> None:
        """
        Create an :class:`AcceptEncodingInvalidHeader` instance.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @overload
    def __add__(self, other: AcceptEncodingValidHeader | Literal[""]) -> AcceptEncodingValidHeader:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str`` header value
        * a ``dict``, with content-coding, ``identity`` or ``*`` ``str``'s as
          keys, and qvalue ``float``'s as values
        * a ``tuple`` or ``list``, where each item is either a header element
          ``str``, or a (content-coding/``identity``/``*``, qvalue) ``tuple``
          or ``list``
        * an :class:`AcceptEncodingValidHeader`,
          :class:`AcceptEncodingNoHeader`, or
          :class:`AcceptEncodingInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or an
        :class:`AcceptEncodingValidHeader` instance, then a new
        :class:`AcceptEncodingValidHeader` instance with the valid header value
        is returned.

        If `other` is ``None``, an :class:`AcceptEncodingNoHeader` instance, an
        invalid header value, or an :class:`AcceptEncodingInvalidHeader`
        instance, a new :class:`AcceptEncodingNoHeader` instance is returned.
        """

    @overload
    def __add__(self, other: AcceptEncodingInvalidHeader | AcceptEncodingNoHeader | None) -> AcceptEncodingNoHeader: ...
    @overload
    def __add__(
        self,
        other: (
            _AnyAcceptEncodingHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> AcceptEncodingValidHeader | AcceptEncodingNoHeader: ...
    @overload
    def __radd__(self, other: AcceptEncodingValidHeader | Literal[""]) -> AcceptEncodingValidHeader:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptEncodingValidHeader.__add__`.
        """

    @overload
    def __radd__(self, other: AcceptEncodingInvalidHeader | AcceptEncodingNoHeader | None) -> AcceptEncodingNoHeader: ...
    @overload
    def __radd__(
        self,
        other: (
            _AnyAcceptEncodingHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> AcceptEncodingValidHeader | AcceptEncodingNoHeader: ...

@overload
def create_accept_encoding_header(header_value: AcceptEncodingValidHeader | Literal[""]) -> AcceptEncodingValidHeader:
    """
    Create an object representing the ``Accept-Encoding`` header in a request.

    :param header_value: (``str``) header value
    :return: If `header_value` is ``None``, an :class:`AcceptEncodingNoHeader`
             instance.

             | If `header_value` is a valid ``Accept-Encoding`` header, an
               :class:`AcceptEncodingValidHeader` instance.

             | If `header_value` is an invalid ``Accept-Encoding`` header, an
               :class:`AcceptEncodingInvalidHeader` instance.
    """

@overload
def create_accept_encoding_header(header_value: AcceptEncodingInvalidHeader) -> AcceptEncodingInvalidHeader: ...
@overload
def create_accept_encoding_header(header_value: AcceptEncodingNoHeader | None) -> AcceptEncodingNoHeader: ...
@overload
def create_accept_encoding_header(header_value: str) -> AcceptEncodingValidHeader | AcceptEncodingInvalidHeader: ...
@overload
def create_accept_encoding_header(header_value: _AnyAcceptEncodingHeader | str | None) -> _AnyAcceptEncodingHeader: ...
def accept_encoding_property() -> _AcceptEncodingProperty: ...

class AcceptLanguage:
    """
    Represent an ``Accept-Language`` header.

    Base class for :class:`AcceptLanguageValidHeader`,
    :class:`AcceptLanguageNoHeader`, and :class:`AcceptLanguageInvalidHeader`.
    """

    @classmethod
    def parse(cls, value: str) -> Iterator[tuple[str, float]]:
        """
        Parse an ``Accept-Language`` header.

        :param value: (``str``) header value
        :return: If `value` is a valid ``Accept-Language`` header, returns an
                 iterator of (language range, quality value) tuples, as parsed
                 from the header from left to right.
        :raises ValueError: if `value` is an invalid header
        """

class AcceptLanguageValidHeader(AcceptLanguage):
    """
    Represent a valid ``Accept-Language`` header.

    A valid header is one that conforms to :rfc:`RFC 7231, section 5.3.5
    <7231#section-5.3.5>`.

    We take the reference from the ``language-range`` syntax rule in :rfc:`RFC
    7231, section 5.3.5 <7231#section-5.3.5>` to :rfc:`RFC 4647, section 2.1
    <4647#section-2.1>` to mean that only basic language ranges (and not
    extended language ranges) are expected in the ``Accept-Language`` header.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptLanguageValidHeader.__add__`).
    """

    def __init__(self, header_value: str) -> None:
        """
        Create an :class:`AcceptLanguageValidHeader` instance.

        :param header_value: (``str``) header value.
        :raises ValueError: if `header_value` is an invalid value for an
                            ``Accept-Language`` header.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @property
    def header_value(self) -> str:
        """(``str`` or ``None``) The header value."""

    @property
    def parsed(self) -> list[tuple[str, float]]:
        """
        (``list`` or ``None``) Parsed form of the header.

        A list of (language range, quality value) tuples.
        """

    def __add__(
        self,
        other: (
            _AnyAcceptLanguageHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str``
        * a ``dict``, with language ranges as keys and qvalues as values
        * a ``tuple`` or ``list``, of language range ``str``'s or of ``tuple``
          or ``list`` (language range, qvalue) pairs (``str``'s and pairs can
          be mixed within the ``tuple`` or ``list``)
        * an :class:`AcceptLanguageValidHeader`,
          :class:`AcceptLanguageNoHeader`, or
          :class:`AcceptLanguageInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or another
        :class:`AcceptLanguageValidHeader` instance, the two header values are
        joined with ``', '``, and a new :class:`AcceptLanguageValidHeader`
        instance with the new header value is returned.

        If `other` is ``None``, an :class:`AcceptLanguageNoHeader` instance, an
        invalid header value, or an :class:`AcceptLanguageInvalidHeader`
        instance, a new :class:`AcceptLanguageValidHeader` instance with the
        same header value as ``self`` is returned.
        """

    def __bool__(self) -> Literal[True]:
        """
        Return whether ``self`` represents a valid ``Accept-Language`` header.

        Return ``True`` if ``self`` represents a valid header, and ``False`` if
        it represents an invalid header, or the header not being in the
        request.

        For this class, it always returns ``True``.
        """

    def __contains__(self, offer: str) -> bool:
        """
        Return ``bool`` indicating whether `offer` is acceptable.

        .. warning::

           The behavior of :meth:`AcceptLanguageValidHeader.__contains__` is
           currently being maintained for backward compatibility, but it will
           change in the future to better conform to the RFC.

           What is 'acceptable' depends on the needs of your application.
           :rfc:`RFC 7231, section 5.3.5 <7231#section-5.3.5>` suggests three
           matching schemes from :rfc:`RFC 4647 <4647>`, two of which WebOb
           supports with :meth:`AcceptLanguageValidHeader.basic_filtering` and
           :meth:`AcceptLanguageValidHeader.lookup` (we interpret the RFC to
           mean that Extended Filtering cannot apply for the
           ``Accept-Language`` header, as the header only accepts basic
           language ranges.) If these are not suitable for the needs of your
           application, you may need to write your own matching using
           :attr:`AcceptLanguageValidHeader.parsed`.

        :param offer: (``str``) language tag offer
        :return: (``bool``) Whether ``offer`` is acceptable according to the
                 header.

        This uses the old criterion of a match in
        :meth:`AcceptLanguageValidHeader._old_match`, which does not conform to
        :rfc:`RFC 7231, section 5.3.5 <7231#section-5.3.5>` or any of the
        matching schemes suggested there. It also does not properly take into
        account ranges with ``q=0`` in the header::

            >>> 'en-gb' in AcceptLanguageValidHeader('en, en-gb;q=0')
            True
            >>> 'en' in AcceptLanguageValidHeader('en;q=0, *')
            True

        (See the docstring for :meth:`AcceptLanguageValidHeader._old_match` for
        other problems with the old criterion for a match.)
        """

    def __iter__(self) -> Iterator[str]:
        """
        Return all the ranges with non-0 qvalues, in order of preference.

        .. warning::

           The behavior of this method is currently maintained for backward
           compatibility, but will change in the future.

        :return: iterator of all the language ranges in the header with non-0
                 qvalues, in descending order of qvalue. If two ranges have the
                 same qvalue, they are returned in the order of their positions
                 in the header, from left to right.

        Please note that this is a simple filter for the ranges in the header
        with non-0 qvalues, and is not necessarily the same as what the client
        prefers, e.g. ``'en-gb;q=0, *'`` means 'everything but British
        English', but ``list(instance)`` would return only ``['*']``.
        """

    def __radd__(
        self,
        other: (
            _AnyAcceptLanguageHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptLanguageValidHeader.__add__`.
        """

    def basic_filtering(self, language_tags: Sequence[str]) -> list[tuple[str, float]]:
        """
        Return the tags that match the header, using Basic Filtering.

        This is an implementation of the Basic Filtering matching scheme,
        suggested as a matching scheme for the ``Accept-Language`` header in
        :rfc:`RFC 7231, section 5.3.5 <7231#section-5.3.5>`, and defined in
        :rfc:`RFC 4647, section 3.3.1 <4647#section-3.3.1>`. It filters the
        tags in the `language_tags` argument and returns the ones that match
        the header according to the matching scheme.

        :param language_tags: (``iterable``) language tags
        :return: A list of tuples of the form (language tag, qvalue), in
                 descending order of qvalue. If two or more tags have the same
                 qvalue, they are returned in the same order as that in the
                 header of the ranges they matched. If the matched range is the
                 same for two or more tags (i.e. their matched ranges have the
                 same qvalue and the same position in the header), then they
                 are returned in the same order as that in the `language_tags`
                 argument. If `language_tags` is unordered, e.g. if it is a set
                 or a dict, then that order may not be reliable.

        For each tag in `language_tags`:

        1. If the tag matches a non-``*`` language range in the header with
           ``q=0`` (meaning "not acceptable", see :rfc:`RFC 7231, section 5.3.1
           <7231#section-5.3.1>`), the tag is filtered out.
        2. The non-``*`` language ranges in the header that do not have ``q=0``
           are considered in descending order of qvalue; where two or more
           language ranges have the same qvalue, they are considered in the
           order in which they appear in the header.
        3. A language range 'matches a particular language tag if, in a
           case-insensitive comparison, it exactly equals the tag, or if it
           exactly equals a prefix of the tag such that the first character
           following the prefix is "-".' (:rfc:`RFC 4647, section 3.3.1
           <4647#section-3.3.1>`)
        4. If the tag does not match any of the non-``*`` language ranges, and
           there is a ``*`` language range in the header, then if the ``*``
           language range has ``q=0``, the language tag is filtered out,
           otherwise the tag is considered a match.

        (If a range (``*`` or non-``*``) appears in the header more than once
        -- this would not make sense, but is nonetheless a valid header
        according to the RFC -- the first in the header is used for matching,
        and the others are ignored.)
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: None = None) -> str | None:
        """
        Return the best match from the sequence of language tag `offers`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future.

           :meth:`AcceptLanguageValidHeader.best_match` uses its own algorithm
           (one not specified in :rfc:`RFC 7231 <7231>`) to determine what is a
           best match. The algorithm has many issues, and does not conform to
           :rfc:`RFC 7231 <7231>`.

           :meth:`AcceptLanguageValidHeader.lookup` is a possible alternative
           for finding a best match -- it conforms to, and is suggested as a
           matching scheme for the ``Accept-Language`` header in, :rfc:`RFC
           7231, section 5.3.5 <7231#section-5.3.5>` -- but please be aware
           that there are differences in how it determines what is a best
           match. If that is not suitable for the needs of your application,
           you may need to write your own matching using
           :attr:`AcceptLanguageValidHeader.parsed`.

        Each language tag in `offers` is checked against each non-0 range in
        the header. If the two are a match according to WebOb's old criterion
        for a match, the quality value of the match is the qvalue of the
        language range from the header multiplied by the server quality value
        of the offer (if the server quality value is not supplied, it is 1).

        The offer in the match with the highest quality value is the best
        match. If there is more than one match with the highest qvalue, the
        match where the language range has a lower number of '*'s is the best
        match. If the two have the same number of '*'s, the one that shows up
        first in `offers` is the best match.

        :param offers: (iterable)

                       | Each item in the iterable may be a ``str`` language
                         tag, or a (language tag, server quality value)
                         ``tuple`` or ``list``. (The two may be mixed in the
                         iterable.)

        :param default_match: (optional, any type) the value to be returned if
                              there is no match

        :return: (``str``, or the type of `default_match`)

                 | The language tag that is the best match. If there is no
                   match, the value of `default_match` is returned.


        **Issues**:

        - Incorrect tiebreaking when quality values of two matches are the same
          (https://github.com/Pylons/webob/issues/256)::

              >>> header = AcceptLanguageValidHeader(
              ...     header_value='en-gb;q=1, en;q=0.8'
              ... )
              >>> header.best_match(offers=['en', 'en-GB'])
              'en'
              >>> header.best_match(offers=['en-GB', 'en'])
              'en-GB'

              >>> header = AcceptLanguageValidHeader(header_value='en-gb, en')
              >>> header.best_match(offers=['en', 'en-gb'])
              'en'
              >>> header.best_match(offers=['en-gb', 'en'])
              'en-gb'

        - Incorrect handling of ``q=0``::

              >>> header = AcceptLanguageValidHeader(header_value='en;q=0, *')
              >>> header.best_match(offers=['en'])
              'en'

              >>> header = AcceptLanguageValidHeader(header_value='fr, en;q=0')
              >>> header.best_match(offers=['en-gb'], default_match='en')
              'en'

        - Matching only takes into account the first subtag when matching a
          range with more specific or less specific tags::

              >>> header = AcceptLanguageValidHeader(header_value='zh')
              >>> header.best_match(offers=['zh-Hans-CN'])
              'zh-Hans-CN'
              >>> header = AcceptLanguageValidHeader(header_value='zh-Hans')
              >>> header.best_match(offers=['zh-Hans-CN'])
              >>> header.best_match(offers=['zh-Hans-CN']) is None
              True

              >>> header = AcceptLanguageValidHeader(header_value='zh-Hans-CN')
              >>> header.best_match(offers=['zh'])
              'zh'
              >>> header.best_match(offers=['zh-Hans'])
              >>> header.best_match(offers=['zh-Hans']) is None
              True

        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: str) -> str: ...
    @overload
    def lookup(
        self, language_tags: Sequence[str], default_range: str | None, default_tag: str, default: None = None
    ) -> str | None:
        """
        Return the language tag that best matches the header, using Lookup.

        This is an implementation of the Lookup matching scheme,
        suggested as a matching scheme for the ``Accept-Language`` header in
        :rfc:`RFC 7231, section 5.3.5 <7231#section-5.3.5>`, and described in
        :rfc:`RFC 4647, section 3.4 <4647#section-3.4>`.

        Each language range in the header is considered in turn, by descending
        order of qvalue; where qvalues are tied, ranges are considered from
        left to right.

        Each language range in the header represents the most specific tag that
        is an acceptable match: Lookup progressively truncates subtags from the
        end of the range until a matching language tag is found. An example is
        given in :rfc:`RFC 4647, section 3.4 <4647#section-3.4>`, under
        "Example of a Lookup Fallback Pattern":

        ::

            Range to match: zh-Hant-CN-x-private1-private2
            1. zh-Hant-CN-x-private1-private2
            2. zh-Hant-CN-x-private1
            3. zh-Hant-CN
            4. zh-Hant
            5. zh
            6. (default)

        :param language_tags: (``iterable``) language tags

        :param default_range: (optional, ``None`` or ``str``)

                              | If Lookup finds no match using the ranges in
                                the header, and this argument is not None,
                                Lookup will next attempt to match the range in
                                this argument, using the same subtag
                                truncation.

                              | `default_range` cannot be '*', as '*' is
                                skipped in Lookup. See :ref:`note
                                <acceptparse-lookup-asterisk-note>`.

                              | This parameter corresponds to the functionality
                                described in :rfc:`RFC 4647, section 3.4.1
                                <4647#section-3.4.1>`, in the paragraph
                                starting with "One common way to provide for a
                                default is to allow a specific language range
                                to be set as the default..."

        :param default_tag: (optional, ``None`` or ``str``)

                            | At least one of `default_tag` or `default` must
                              be supplied as an argument to the method, to
                              define the defaulting behaviour.

                            | If Lookup finds no match using the ranges in the
                              header and `default_range`, this argument is not
                              ``None``, and it does not match any range in the
                              header with ``q=0`` (exactly, with no subtag
                              truncation), then this value is returned.

                            | This parameter corresponds to "return a
                              particular language tag designated for the
                              operation", one of the examples of "defaulting
                              behavior" described in :rfc:`RFC 4647, section
                              3.4.1 <4647#section-3.4.1>`.

        :param default: (optional, ``None`` or any type, including a callable)

                        | At least one of `default_tag` or `default` must be
                          supplied as an argument to the method, to define the
                          defaulting behaviour.

                        | If Lookup finds no match using the ranges in the
                          header and `default_range`, and `default_tag` is
                          ``None`` or not acceptable because it matches a
                          ``q=0`` range in the header, then Lookup will next
                          examine the `default` argument.

                        | If `default` is a callable, it will be called, and
                          the callable's return value will be returned.

                        | If `default` is not a callable, the value itself will
                          be returned.

                        | The difference between supplying a ``str`` to
                          `default_tag` and `default` is that `default_tag` is
                          checked against ``q=0`` ranges in the header to see
                          if it matches one of the ranges specified as not
                          acceptable, whereas a ``str`` for the `default`
                          argument is simply returned.

                        | This parameter corresponds to the "defaulting
                          behavior" described in :rfc:`RFC 4647, section 3.4.1
                          <4647#section-3.4.1>`

        :return: (``str``, ``None``, or any type)

                 | The best match according to the Lookup matching scheme, or a
                   return value from one of the default arguments.

        **Notes**:

        .. _acceptparse-lookup-asterisk-note:

        - Lookup's behaviour with '*' language ranges in the header may be
          surprising. From :rfc:`RFC 4647, section 3.4 <4647#section-3.4>`:

              In the lookup scheme, this range does not convey enough
              information by itself to determine which language tag is most
              appropriate, since it matches everything.  If the language range
              "*" is followed by other language ranges, it is skipped.  If the
              language range "*" is the only one in the language priority list
              or if no other language range follows, the default value is
              computed and returned.

          So

          ::

              >>> header = AcceptLanguageValidHeader('de, zh, *')
              >>> header.lookup(language_tags=['ja', 'en'], default='default')
              'default'

        - Any tags in `language_tags` and `default_tag` and any tag matched
          during the subtag truncation search for `default_range`, that are an
          exact match for a non-``*`` range with ``q=0`` in the header, are
          considered not acceptable and ruled out.

        - If there is a ``*;q=0`` in the header, then `default_range` and
          `default_tag` have no effect, as ``*;q=0`` means that all languages
          not already matched by other ranges within the header are
          unacceptable.
        """

    @overload
    def lookup(
        self, language_tags: Sequence[str], *, default_range: str | None = None, default_tag: str, default: None = None
    ) -> str | None: ...
    @overload
    def lookup(
        self, language_tags: Sequence[str], default_range: str | None, default_tag: None, default: _T | Callable[[], _T]
    ) -> _T | str | None: ...
    @overload
    def lookup(
        self, language_tags: Sequence[str], default_range: str | None, default_tag: str, default: _T | Callable[[], _T]
    ) -> _T | str: ...
    @overload
    def lookup(
        self,
        language_tags: Sequence[str],
        *,
        default_range: str | None = None,
        default_tag: None = None,
        default: _T | Callable[[], _T],
    ) -> _T | str | None: ...
    @overload
    def lookup(
        self, language_tags: Sequence[str], *, default_range: str | None = None, default_tag: str, default: _T | Callable[[], _T]
    ) -> _T | str: ...
    def quality(self, offer: str) -> float | None:
        """
        Return quality value of given offer, or ``None`` if there is no match.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future.

           :meth:`AcceptLanguageValidHeader.quality` uses its own algorithm
           (one not specified in :rfc:`RFC 7231 <7231>`) to determine what is a
           best match. The algorithm has many issues, and does not conform to
           :rfc:`RFC 7231 <7231>`.

           What should be considered a match depends on the needs of your
           application (for example, should a language range in the header
           match a more specific language tag offer, or a less specific tag
           offer?) :rfc:`RFC 7231, section 5.3.5 <7231#section-5.3.5>` suggests
           three matching schemes from :rfc:`RFC 4647 <4647>`, two of which
           WebOb supports with
           :meth:`AcceptLanguageValidHeader.basic_filtering` and
           :meth:`AcceptLanguageValidHeader.lookup` (we interpret the RFC to
           mean that Extended Filtering cannot apply for the
           ``Accept-Language`` header, as the header only accepts basic
           language ranges.) :meth:`AcceptLanguageValidHeader.basic_filtering`
           returns quality values with the matched language tags.
           :meth:`AcceptLanguageValidHeader.lookup` returns a language tag
           without the quality value, but the quality value is less likely to
           be useful when we are looking for a best match.

           If these are not suitable or sufficient for the needs of your
           application, you may need to write your own matching using
           :attr:`AcceptLanguageValidHeader.parsed`.

        :param offer: (``str``) language tag offer
        :return: (``float`` or ``None``)

                 | The highest quality value from the language range(s) that
                   match the `offer`, or ``None`` if there is no match.


        **Issues**:

        - Incorrect handling of ``q=0`` and ``*``::

              >>> header = AcceptLanguageValidHeader(header_value='en;q=0, *')
              >>> header.quality(offer='en')
              1.0

        - Matching only takes into account the first subtag when matching a
          range with more specific or less specific tags::

              >>> header = AcceptLanguageValidHeader(header_value='zh')
              >>> header.quality(offer='zh-Hans-CN')
              1.0
              >>> header = AcceptLanguageValidHeader(header_value='zh-Hans')
              >>> header.quality(offer='zh-Hans-CN')
              >>> header.quality(offer='zh-Hans-CN') is None
              True

              >>> header = AcceptLanguageValidHeader(header_value='zh-Hans-CN')
              >>> header.quality(offer='zh')
              1.0
              >>> header.quality(offer='zh-Hans')
              >>> header.quality(offer='zh-Hans') is None
              True

        """

class _AcceptLanguageInvalidOrNoHeader(AcceptLanguage):
    """
    Represent when an ``Accept-Language`` header is invalid or not in request.

    This is the base class for the behaviour that
    :class:`.AcceptLanguageInvalidHeader` and :class:`.AcceptLanguageNoHeader`
    have in common.

    :rfc:`7231` does not provide any guidance on what should happen if the
    ``Accept-Language`` header has an invalid value. This implementation
    disregards the header when the header is invalid, so
    :class:`.AcceptLanguageInvalidHeader` and :class:`.AcceptLanguageNoHeader`
    have much behaviour in common.
    """

    def __bool__(self) -> Literal[False]:
        """
        Return whether ``self`` represents a valid ``Accept-Language`` header.

        Return ``True`` if ``self`` represents a valid header, and ``False`` if
        it represents an invalid header, or the header not being in the
        request.

        For this class, it always returns ``False``.
        """

    def __contains__(self, offer: str) -> Literal[True]:
        """
        Return ``bool`` indicating whether `offer` is acceptable.

        .. warning::

           The behavior of ``.__contains__`` for the ``AcceptLanguage`` classes
           is currently being maintained for backward compatibility, but it
           will change in the future to better conform to the RFC.

        :param offer: (``str``) language tag offer
        :return: (``bool``) Whether ``offer`` is acceptable according to the
                 header.

        For this class, either there is no ``Accept-Language`` header in the
        request, or the header is invalid, so any language tag is acceptable,
        and this always returns ``True``.
        """

    def __iter__(self) -> Iterator[str]:
        """
        Return all the ranges with non-0 qvalues, in order of preference.

        .. warning::

           The behavior of this method is currently maintained for backward
           compatibility, but will change in the future.

        :return: iterator of all the language ranges in the header with non-0
                 qvalues, in descending order of qvalue. If two ranges have the
                 same qvalue, they are returned in the order of their positions
                 in the header, from left to right.

        For this class, either there is no ``Accept-Language`` header in the
        request, or the header is invalid, so there are no language ranges, and
        this always returns an empty iterator.
        """

    def basic_filtering(self, language_tags: Iterable[str]) -> list[tuple[str, float]]:
        """
        Return the tags that match the header, using Basic Filtering.

        :param language_tags: (``iterable``) language tags
        :return: A list of tuples of the form (language tag, qvalue), in
                 descending order of preference.

        When the header is invalid and when the header is not in the request,
        there are no matches, so this method always returns an empty list.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: None = None) -> str | None:
        """
        Return the best match from the sequence of language tag `offers`.

        This is the ``.best_match()`` method for when the header is invalid or
        not found in the request, corresponding to
        :meth:`AcceptLanguageValidHeader.best_match`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future (see the documentation for
           :meth:`AcceptLanguageValidHeader.best_match`).

        When the header is invalid, or there is no `Accept-Language` header in
        the request, any of the language tags in `offers` are considered
        acceptable, so the best match is the tag in `offers` with the highest
        server quality value (if the server quality value is not supplied, it
        is 1).

        If more than one language tags in `offers` have the same highest server
        quality value, then the one that shows up first in `offers` is the best
        match.

        :param offers: (iterable)

                       | Each item in the iterable may be a ``str`` language
                         tag, or a (language tag, server quality value)
                         ``tuple`` or ``list``. (The two may be mixed in the
                         iterable.)

        :param default_match: (optional, any type) the value to be returned if
                              `offers` is empty.

        :return: (``str``, or the type of `default_match`)

                 | The language tag that has the highest server quality value.
                   If `offers` is empty, the value of `default_match` is
                   returned.
        """

    @overload
    def best_match(self, offers: Iterable[str | tuple[str, float] | list[Any]], default_match: str) -> str: ...
    @overload
    def lookup(self, language_tags: object, default_range: object, default_tag: str, default: object = None) -> str:
        """
        Return the language tag that best matches the header, using Lookup.

        When the header is invalid, or there is no ``Accept-Language`` header
        in the request, all language tags are considered acceptable, so it is
        as if the header is '*'. As specified for the Lookup matching scheme in
        :rfc:`RFC 4647, section 3.4 <4647#section-3.4>`, when the header is
        '*', the default value is to be computed and returned. So this method
        will ignore the `language_tags` and `default_range` arguments, and
        proceed to `default_tag`, then `default`.

        :param language_tags: (optional, any type)

                              | This argument is ignored, and is only used as a
                                placeholder so that the method signature
                                corresponds to that of
                                :meth:`AcceptLanguageValidHeader.lookup`.

        :param default_range: (optional, any type)

                              | This argument is ignored, and is only used as a
                                placeholder so that the method signature
                                corresponds to that of
                                :meth:`AcceptLanguageValidHeader.lookup`.

        :param default_tag: (optional, ``None`` or ``str``)

                            | At least one of `default_tag` or `default` must
                              be supplied as an argument to the method, to
                              define the defaulting behaviour.

                            | If this argument is not ``None``, then it is
                              returned.

                            | This parameter corresponds to "return a
                              particular language tag designated for the
                              operation", one of the examples of "defaulting
                              behavior" described in :rfc:`RFC 4647, section
                              3.4.1 <4647#section-3.4.1>`.

        :param default: (optional, ``None`` or any type, including a callable)

                        | At least one of `default_tag` or `default` must be
                          supplied as an argument to the method, to define the
                          defaulting behaviour.

                        | If `default_tag` is ``None``, then Lookup will next
                          examine the `default` argument.

                        | If `default` is a callable, it will be called, and
                          the callable's return value will be returned.

                        | If `default` is not a callable, the value itself will
                          be returned.

                        | This parameter corresponds to the "defaulting
                          behavior" described in :rfc:`RFC 4647, section 3.4.1
                          <4647#section-3.4.1>`

        :return: (``str``, or any type)

                 | the return value from `default_tag` or `default`.
        """

    @overload
    def lookup(
        self, language_tags: object = None, *, default_range: object = None, default_tag: str, default: object = None
    ) -> str: ...
    @overload
    def lookup(self, language_tags: object, default_range: object, default_tag: None, default: _T | Callable[[], _T]) -> _T: ...
    @overload
    def lookup(
        self,
        language_tags: object = None,
        *,
        default_range: object = None,
        default_tag: None = None,
        default: _T | Callable[[], _T],
    ) -> _T: ...
    def quality(self, offer: str) -> float | None:
        """
        Return quality value of given offer, or ``None`` if there is no match.

        This is the ``.quality()`` method for when the header is invalid or not
        found in the request, corresponding to
        :meth:`AcceptLanguageValidHeader.quality`.

        .. warning::

           This is currently maintained for backward compatibility, and will be
           deprecated in the future (see the documentation for
           :meth:`AcceptLanguageValidHeader.quality`).

        :param offer: (``str``) language tag offer
        :return: (``float``) ``1.0``.

        When the ``Accept-Language`` header is invalid or not in the request,
        all offers are equally acceptable, so 1.0 is always returned.
        """

class AcceptLanguageNoHeader(_AcceptLanguageInvalidOrNoHeader):
    """
    Represent when there is no ``Accept-Language`` header in the request.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptLanguageNoHeader.__add__`).
    """

    def __init__(self) -> None:
        """
        Create an :class:`AcceptLanguageNoHeader` instance.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @property
    def header_value(self) -> None:
        """
        (``str`` or ``None``) The header value.

        As there is no header in the request, this is ``None``.
        """

    @property
    def parsed(self) -> None:
        """
        (``list`` or ``None``) Parsed form of the header.

        As there is no header in the request, this is ``None``.
        """

    @overload
    def __add__(self, other: AcceptLanguageValidHeader) -> AcceptLanguageValidHeader:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str``
        * a ``dict``, with language ranges as keys and qvalues as values
        * a ``tuple`` or ``list``, of language range ``str``'s or of ``tuple``
          or ``list`` (language range, qvalue) pairs (``str``'s and pairs can be
          mixed within the ``tuple`` or ``list``)
        * an :class:`AcceptLanguageValidHeader`,
          :class:`AcceptLanguageNoHeader`, or
          :class:`AcceptLanguageInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or an
        :class:`AcceptLanguageValidHeader` instance, a new
        :class:`AcceptLanguageValidHeader` instance with the valid header value
        is returned.

        If `other` is ``None``, an :class:`AcceptLanguageNoHeader` instance, an
        invalid header value, or an :class:`AcceptLanguageInvalidHeader`
        instance, a new :class:`AcceptLanguageNoHeader` instance is returned.
        """

    @overload
    def __add__(self, other: AcceptLanguageInvalidHeader | AcceptLanguageNoHeader | Literal[""] | None) -> Self: ...
    @overload
    def __add__(
        self,
        other: (
            _AnyAcceptLanguageHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self | AcceptLanguageValidHeader: ...
    @overload
    def __radd__(self, other: AcceptLanguageValidHeader) -> AcceptLanguageValidHeader:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptLanguageNoHeader.__add__`.
        """

    @overload
    def __radd__(self, other: AcceptLanguageInvalidHeader | AcceptLanguageNoHeader | Literal[""] | None) -> Self: ...
    @overload
    def __radd__(
        self,
        other: (
            _AnyAcceptLanguageHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> Self | AcceptLanguageValidHeader: ...

class AcceptLanguageInvalidHeader(_AcceptLanguageInvalidOrNoHeader):
    """
    Represent an invalid ``Accept-Language`` header.

    An invalid header is one that does not conform to
    :rfc:`7231#section-5.3.5`. As specified in the RFC, an empty header is an
    invalid ``Accept-Language`` header.

    :rfc:`7231` does not provide any guidance on what should happen if the
    ``Accept-Language`` header has an invalid value. This implementation
    disregards the header, and treats it as if there is no ``Accept-Language``
    header in the request.

    This object should not be modified. To add to the header, we can use the
    addition operators (``+`` and ``+=``), which return a new object (see the
    docstring for :meth:`AcceptLanguageInvalidHeader.__add__`).
    """

    def __init__(self, header_value: str) -> None:
        """
        Create an :class:`AcceptLanguageInvalidHeader` instance.
        """

    def copy(self) -> Self:
        """
        Create a copy of the header object.

        """

    @property
    def header_value(self) -> str:
        """(``str`` or ``None``) The header value."""

    @property
    def parsed(self) -> None:
        """
        (``list`` or ``None``) Parsed form of the header.

        As the header is invalid and cannot be parsed, this is ``None``.
        """

    @overload
    def __add__(self, other: AcceptLanguageValidHeader) -> AcceptLanguageValidHeader:
        """
        Add to header, creating a new header object.

        `other` can be:

        * ``None``
        * a ``str``
        * a ``dict``, with language ranges as keys and qvalues as values
        * a ``tuple`` or ``list``, of language range ``str``'s or of ``tuple``
          or ``list`` (language range, qvalue) pairs (``str``'s and pairs can
          be mixed within the ``tuple`` or ``list``)
        * an :class:`AcceptLanguageValidHeader`,
          :class:`AcceptLanguageNoHeader`, or
          :class:`AcceptLanguageInvalidHeader` instance
        * object of any other type that returns a value for ``__str__``

        If `other` is a valid header value or an
        :class:`AcceptLanguageValidHeader` instance, a new
        :class:`AcceptLanguageValidHeader` instance with the valid header value
        is returned.

        If `other` is ``None``, an :class:`AcceptLanguageNoHeader` instance, an
        invalid header value, or an :class:`AcceptLanguageInvalidHeader`
        instance, a new :class:`AcceptLanguageNoHeader` instance is returned.
        """

    @overload
    def __add__(
        self, other: AcceptLanguageInvalidHeader | AcceptLanguageNoHeader | Literal[""] | None
    ) -> AcceptLanguageNoHeader: ...
    @overload
    def __add__(
        self,
        other: (
            _AnyAcceptLanguageHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> AcceptLanguageValidHeader | AcceptLanguageNoHeader: ...
    @overload
    def __radd__(self, other: AcceptLanguageValidHeader) -> AcceptLanguageValidHeader:
        """
        Add to header, creating a new header object.

        See the docstring for :meth:`AcceptLanguageValidHeader.__add__`.
        """

    @overload
    def __radd__(
        self, other: AcceptLanguageInvalidHeader | AcceptLanguageNoHeader | Literal[""] | None
    ) -> AcceptLanguageNoHeader: ...
    @overload
    def __radd__(
        self,
        other: (
            _AnyAcceptLanguageHeader
            | SupportsItems[str, float]
            | _ListOrTuple[str | tuple[str, float] | list[Any]]
            | _SupportsStr
            | str
            | None
        ),
    ) -> AcceptLanguageValidHeader | AcceptLanguageNoHeader: ...

@overload
def create_accept_language_header(header_value: AcceptLanguageValidHeader | Literal[""]) -> AcceptLanguageValidHeader:
    """
    Create an object representing the ``Accept-Language`` header in a request.

    :param header_value: (``str``) header value
    :return: If `header_value` is ``None``, an :class:`AcceptLanguageNoHeader`
             instance.

             | If `header_value` is a valid ``Accept-Language`` header, an
               :class:`AcceptLanguageValidHeader` instance.

             | If `header_value` is an invalid ``Accept-Language`` header, an
               :class:`AcceptLanguageInvalidHeader` instance.
    """

@overload
def create_accept_language_header(header_value: AcceptLanguageNoHeader | None) -> AcceptLanguageNoHeader: ...
@overload
def create_accept_language_header(header_value: AcceptLanguageInvalidHeader) -> AcceptLanguageInvalidHeader: ...
@overload
def create_accept_language_header(header_value: str) -> AcceptLanguageValidHeader | AcceptLanguageInvalidHeader: ...
@overload
def create_accept_language_header(header_value: _AnyAcceptLanguageHeader | str | None) -> _AnyAcceptLanguageHeader: ...
def accept_language_property() -> _AcceptLanguageProperty: ...
