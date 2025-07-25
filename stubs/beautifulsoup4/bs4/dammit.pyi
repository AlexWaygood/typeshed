"""Beautiful Soup bonus library: Unicode, Dammit

This library converts a bytestream to Unicode through any means
necessary. It is heavily based on code from Mark Pilgrim's Universal
Feed Parser. It works best on XML and HTML, but it does not rewrite the
XML or HTML to reflect a new encoding; that's the tree builder's job.
"""

from _typeshed import Incomplete
from collections.abc import Iterable, Iterator
from logging import Logger
from typing import Any, Literal

def chardet_dammit(s): ...

xml_encoding: str
html_meta: str
encoding_res: Any

class EntitySubstitution:
    """The ability to substitute XML or HTML entities for certain characters."""

    CHARACTER_TO_HTML_ENTITY: Any
    HTML_ENTITY_TO_CHARACTER: Any
    CHARACTER_TO_HTML_ENTITY_RE: Any
    CHARACTER_TO_XML_ENTITY: Any
    BARE_AMPERSAND_OR_BRACKET: Any
    AMPERSAND_OR_BRACKET: Any
    @classmethod
    def quoted_attribute_value(cls, value):
        """Make a value into a quoted XML attribute, possibly escaping it.

        Most strings will be quoted using double quotes.

         Bob's Bar -> "Bob's Bar"

        If a string contains double quotes, it will be quoted using
        single quotes.

         Welcome to "my bar" -> 'Welcome to "my bar"'

        If a string contains both single and double quotes, the
        double quotes will be escaped, and the string will be quoted
        using double quotes.

         Welcome to "Bob's Bar" -> "Welcome to &quot;Bob's bar&quot;
        """

    @classmethod
    def substitute_xml(cls, value, make_quoted_attribute: bool = False):
        """Substitute XML entities for special XML characters.

        :param value: A string to be substituted. The less-than sign
          will become &lt;, the greater-than sign will become &gt;,
          and any ampersands will become &amp;. If you want ampersands
          that appear to be part of an entity definition to be left
          alone, use substitute_xml_containing_entities() instead.

        :param make_quoted_attribute: If True, then the string will be
         quoted, as befits an attribute value.
        """

    @classmethod
    def substitute_xml_containing_entities(cls, value, make_quoted_attribute: bool = False):
        """Substitute XML entities for special XML characters.

        :param value: A string to be substituted. The less-than sign will
          become &lt;, the greater-than sign will become &gt;, and any
          ampersands that are not part of an entity defition will
          become &amp;.

        :param make_quoted_attribute: If True, then the string will be
         quoted, as befits an attribute value.
        """

    @classmethod
    def substitute_html(cls, s):
        """Replace certain Unicode characters with named HTML entities.

        This differs from data.encode(encoding, 'xmlcharrefreplace')
        in that the goal is to make the result more readable (to those
        with ASCII displays) rather than to recover from
        errors. There's absolutely nothing wrong with a UTF-8 string
        containg a LATIN SMALL LETTER E WITH ACUTE, but replacing that
        character with "&eacute;" will make it more readable to some
        people.

        :param s: A Unicode string.
        """

class EncodingDetector:
    """Suggests a number of possible encodings for a bytestring.

    Order of precedence:

    1. Encodings you specifically tell EncodingDetector to try first
    (the known_definite_encodings argument to the constructor).

    2. An encoding determined by sniffing the document's byte-order mark.

    3. Encodings you specifically tell EncodingDetector to try if
    byte-order mark sniffing fails (the user_encodings argument to the
    constructor).

    4. An encoding declared within the bytestring itself, either in an
    XML declaration (if the bytestring is to be interpreted as an XML
    document), or in a <meta> tag (if the bytestring is to be
    interpreted as an HTML document.)

    5. An encoding detected through textual analysis by chardet,
    cchardet, or a similar external library.

    4. UTF-8.

    5. Windows-1252.

    """

    known_definite_encodings: list[str]
    user_encodings: list[str]
    exclude_encodings: set[str]
    chardet_encoding: Incomplete | None
    is_html: bool
    declared_encoding: str | None
    markup: Any
    sniffed_encoding: str | None
    def __init__(
        self,
        markup,
        known_definite_encodings: Iterable[str] | None = None,
        is_html: bool = False,
        exclude_encodings: list[str] | None = None,
        user_encodings: list[str] | None = None,
        override_encodings: list[str] | None = None,
    ) -> None:
        """Constructor.

        :param markup: Some markup in an unknown encoding.

        :param known_definite_encodings: When determining the encoding
            of `markup`, these encodings will be tried first, in
            order. In HTML terms, this corresponds to the "known
            definite encoding" step defined here:
            https://html.spec.whatwg.org/multipage/parsing.html#parsing-with-a-known-character-encoding

        :param user_encodings: These encodings will be tried after the
            `known_definite_encodings` have been tried and failed, and
            after an attempt to sniff the encoding by looking at a
            byte order mark has failed. In HTML terms, this
            corresponds to the step "user has explicitly instructed
            the user agent to override the document's character
            encoding", defined here:
            https://html.spec.whatwg.org/multipage/parsing.html#determining-the-character-encoding

        :param override_encodings: A deprecated alias for
            known_definite_encodings. Any encodings here will be tried
            immediately after the encodings in
            known_definite_encodings.

        :param is_html: If True, this markup is considered to be
            HTML. Otherwise it's assumed to be XML.

        :param exclude_encodings: These encodings will not be tried,
            even if they otherwise would be.

        """

    @property
    def encodings(self) -> Iterator[str]:
        """Yield a number of encodings that might work for this markup.

        :yield: A sequence of strings.
        """

    @classmethod
    def strip_byte_order_mark(cls, data):
        """If a byte-order mark is present, strip it and return the encoding it implies.

        :param data: Some markup.
        :return: A 2-tuple (modified data, implied encoding)
        """

    @classmethod
    def find_declared_encoding(cls, markup, is_html: bool = False, search_entire_document: bool = False) -> str | None:
        """Given a document, tries to find its declared encoding.

        An XML encoding is declared at the beginning of the document.

        An HTML encoding is declared in a <meta> tag, hopefully near the
        beginning of the document.

        :param markup: Some markup.
        :param is_html: If True, this markup is considered to be HTML. Otherwise
            it's assumed to be XML.
        :param search_entire_document: Since an encoding is supposed to declared near the beginning
            of the document, most of the time it's only necessary to search a few kilobytes of data.
            Set this to True to force this method to search the entire document.
        """

class UnicodeDammit:
    """A class for detecting the encoding of a *ML document and
    converting it to a Unicode string. If the source encoding is
    windows-1252, can replace MS smart quotes with their HTML or XML
    equivalents.
    """

    CHARSET_ALIASES: dict[str, str]
    ENCODINGS_WITH_SMART_QUOTES: list[str]
    smart_quotes_to: Literal["ascii", "xml", "html"] | None
    tried_encodings: list[tuple[str, str]]
    contains_replacement_characters: bool
    is_html: bool
    log: Logger
    detector: EncodingDetector
    markup: Any
    unicode_markup: str
    original_encoding: Incomplete | None
    def __init__(
        self,
        markup,
        known_definite_encodings: list[str] | None = [],
        smart_quotes_to: Literal["ascii", "xml", "html"] | None = None,
        is_html: bool = False,
        exclude_encodings: list[str] | None = [],
        user_encodings: list[str] | None = None,
        override_encodings: list[str] | None = None,
    ) -> None:
        """Constructor.

        :param markup: A bytestring representing markup in an unknown encoding.

        :param known_definite_encodings: When determining the encoding
            of `markup`, these encodings will be tried first, in
            order. In HTML terms, this corresponds to the "known
            definite encoding" step defined here:
            https://html.spec.whatwg.org/multipage/parsing.html#parsing-with-a-known-character-encoding

        :param user_encodings: These encodings will be tried after the
            `known_definite_encodings` have been tried and failed, and
            after an attempt to sniff the encoding by looking at a
            byte order mark has failed. In HTML terms, this
            corresponds to the step "user has explicitly instructed
            the user agent to override the document's character
            encoding", defined here:
            https://html.spec.whatwg.org/multipage/parsing.html#determining-the-character-encoding

        :param override_encodings: A deprecated alias for
            known_definite_encodings. Any encodings here will be tried
            immediately after the encodings in
            known_definite_encodings.

        :param smart_quotes_to: By default, Microsoft smart quotes will, like all other characters, be converted
           to Unicode characters. Setting this to 'ascii' will convert them to ASCII quotes instead.
           Setting it to 'xml' will convert them to XML entity references, and setting it to 'html'
           will convert them to HTML entity references.
        :param is_html: If True, this markup is considered to be HTML. Otherwise
            it's assumed to be XML.
        :param exclude_encodings: These encodings will not be considered, even
            if the sniffing code thinks they might make sense.

        """

    @property
    def declared_html_encoding(self) -> str | None:
        """If the markup is an HTML document, returns the encoding declared _within_
        the document.
        """

    def find_codec(self, charset: str) -> str | None:
        """Convert the name of a character set to a codec name.

        :param charset: The name of a character set.
        :return: The name of a codec.
        """
    MS_CHARS: dict[bytes, str | tuple[str, ...]]
    MS_CHARS_TO_ASCII: dict[bytes, str]
    WINDOWS_1252_TO_UTF8: dict[int, bytes]
    MULTIBYTE_MARKERS_AND_SIZES: list[tuple[int, int, int]]
    FIRST_MULTIBYTE_MARKER: int
    LAST_MULTIBYTE_MARKER: int
    @classmethod
    def detwingle(cls, in_bytes: bytes, main_encoding: str = "utf8", embedded_encoding: str = "windows-1252") -> bytes:
        """Fix characters from one encoding embedded in some other encoding.

        Currently the only situation supported is Windows-1252 (or its
        subset ISO-8859-1), embedded in UTF-8.

        :param in_bytes: A bytestring that you suspect contains
            characters from multiple encodings. Note that this _must_
            be a bytestring. If you've already converted the document
            to Unicode, you're too late.
        :param main_encoding: The primary encoding of `in_bytes`.
        :param embedded_encoding: The encoding that was used to embed characters
            in the main document.
        :return: A bytestring in which `embedded_encoding`
          characters have been converted to their `main_encoding`
          equivalents.
        """
