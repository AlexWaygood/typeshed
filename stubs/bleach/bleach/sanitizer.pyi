from collections.abc import Callable, Container, Iterable, Iterator
from re import Pattern
from typing import Final, Protocol, type_check_only
from typing_extensions import TypeAlias

from html5lib.filters.base import Filter
from html5lib.filters.sanitizer import Filter as SanitizerFilter
from html5lib.treewalkers.base import TreeWalker

from . import _HTMLAttrKey
from .css_sanitizer import CSSSanitizer
from .html5lib_shim import BleachHTMLParser, BleachHTMLSerializer
from .linkifier import _Token

ALLOWED_TAGS: Final[frozenset[str]]
ALLOWED_ATTRIBUTES: Final[dict[str, list[str]]]
ALLOWED_PROTOCOLS: Final[frozenset[str]]

INVISIBLE_CHARACTERS: Final[str]
INVISIBLE_CHARACTERS_RE: Final[Pattern[str]]
INVISIBLE_REPLACEMENT_CHAR: Final = "?"

class NoCssSanitizerWarning(UserWarning): ...

@type_check_only
class _FilterConstructor(Protocol):
    def __call__(self, *, source: BleachSanitizerFilter) -> Filter: ...

# _FilterConstructor used to be called _Filter
# this alias is obsolete and can potentially be removed in the future
_Filter: TypeAlias = _FilterConstructor  # noqa: Y047

_AttributeFilter: TypeAlias = Callable[[str, str, str], bool]
_AttributeDict: TypeAlias = dict[str, list[str] | _AttributeFilter] | dict[str, list[str]] | dict[str, _AttributeFilter]
_Attributes: TypeAlias = _AttributeFilter | _AttributeDict | list[str]

class Cleaner:
    """Cleaner for cleaning HTML fragments of malicious content

    This cleaner is a security-focused function whose sole purpose is to remove
    malicious content from a string such that it can be displayed as content in
    a web page.

    To use::

        from bleach.sanitizer import Cleaner

        cleaner = Cleaner()

        for text in all_the_yucky_things:
            sanitized = cleaner.clean(text)

    .. Note::

       This cleaner is not designed to use to transform content to be used in
       non-web-page contexts.

    .. Warning::

       This cleaner is not thread-safe--the html parser has internal state.
       Create a separate cleaner per thread!


    """

    tags: Iterable[str]
    attributes: _Attributes
    protocols: Iterable[str]
    strip: bool
    strip_comments: bool
    filters: Iterable[Filter]
    css_sanitizer: CSSSanitizer | None
    parser: BleachHTMLParser
    walker: TreeWalker
    serializer: BleachHTMLSerializer
    def __init__(
        self,
        tags: Iterable[str] = ...,
        attributes: _Attributes = ...,
        protocols: Iterable[str] = ...,
        strip: bool = False,
        strip_comments: bool = True,
        filters: Iterable[_FilterConstructor] | None = None,
        css_sanitizer: CSSSanitizer | None = None,
    ) -> None:
        """Initializes a Cleaner

        :arg set tags: set of allowed tags; defaults to
            ``bleach.sanitizer.ALLOWED_TAGS``

        :arg dict attributes: allowed attributes; can be a callable, list or dict;
            defaults to ``bleach.sanitizer.ALLOWED_ATTRIBUTES``

        :arg list protocols: allowed list of protocols for links; defaults
            to ``bleach.sanitizer.ALLOWED_PROTOCOLS``

        :arg bool strip: whether or not to strip disallowed elements

        :arg bool strip_comments: whether or not to strip HTML comments

        :arg list filters: list of html5lib Filter classes to pass streamed content through

            .. seealso:: http://html5lib.readthedocs.io/en/latest/movingparts.html#filters

            .. Warning::

               Using filters changes the output of ``bleach.Cleaner.clean``.
               Make sure the way the filters change the output are secure.

        :arg CSSSanitizer css_sanitizer: instance with a "sanitize_css" method for
            sanitizing style attribute values and style text; defaults to None

        """

    def clean(self, text: str) -> str:
        """Cleans text and returns sanitized result as unicode

        :arg str text: text to be cleaned

        :returns: sanitized text as unicode

        :raises TypeError: if ``text`` is not a text type

        """

def attribute_filter_factory(attributes: _Attributes) -> _AttributeFilter:
    """Generates attribute filter function for the given attributes value

    The attributes value can take one of several shapes. This returns a filter
    function appropriate to the attributes value. One nice thing about this is
    that there's less if/then shenanigans in the ``allow_token`` method.

    """

class BleachSanitizerFilter(SanitizerFilter):
    """html5lib Filter that sanitizes text

    This filter can be used anywhere html5lib filters can be used.

    """

    allowed_tags: frozenset[str]
    allowed_protocols: frozenset[str]
    attr_filter: _AttributeFilter
    strip_disallowed_tags: bool
    strip_html_comments: bool
    attr_val_is_uri: frozenset[_HTMLAttrKey]
    svg_attr_val_allows_ref: frozenset[_HTMLAttrKey]
    svg_allow_local_href: frozenset[_HTMLAttrKey]
    css_sanitizer: CSSSanitizer | None
    def __init__(
        self,
        source: TreeWalker,
        allowed_tags: Iterable[str] = ...,
        attributes: _Attributes = ...,
        allowed_protocols: Iterable[str] = ...,
        attr_val_is_uri: frozenset[_HTMLAttrKey] = ...,
        svg_attr_val_allows_ref: frozenset[_HTMLAttrKey] = ...,
        svg_allow_local_href: frozenset[_HTMLAttrKey] = ...,
        strip_disallowed_tags: bool = False,
        strip_html_comments: bool = True,
        css_sanitizer: CSSSanitizer | None = None,
    ) -> None:
        """Creates a BleachSanitizerFilter instance

        :arg source: html5lib TreeWalker stream as an html5lib TreeWalker

        :arg set allowed_tags: set of allowed tags; defaults to
            ``bleach.sanitizer.ALLOWED_TAGS``

        :arg dict attributes: allowed attributes; can be a callable, list or dict;
            defaults to ``bleach.sanitizer.ALLOWED_ATTRIBUTES``

        :arg list allowed_protocols: allowed list of protocols for links; defaults
            to ``bleach.sanitizer.ALLOWED_PROTOCOLS``

        :arg attr_val_is_uri: set of attributes that have URI values

        :arg svg_attr_val_allows_ref: set of SVG attributes that can have
            references

        :arg svg_allow_local_href: set of SVG elements that can have local
            hrefs

        :arg bool strip_disallowed_tags: whether or not to strip disallowed
            tags

        :arg bool strip_html_comments: whether or not to strip HTML comments

        :arg CSSSanitizer css_sanitizer: instance with a "sanitize_css" method for
            sanitizing style attribute values and style text; defaults to None

        """

    def sanitize_stream(self, token_iterator: Iterable[_Token]) -> Iterator[_Token]: ...
    def merge_characters(self, token_iterator: Iterable[_Token]) -> Iterator[_Token]:
        """Merge consecutive Characters tokens in a stream"""

    def __iter__(self) -> Iterator[_Token]: ...
    def sanitize_token(self, token: _Token) -> _Token | list[_Token] | None:
        """Sanitize a token either by HTML-encoding or dropping.

        Unlike sanitizer.Filter, allowed_attributes can be a dict of {'tag':
        ['attribute', 'pairs'], 'tag': callable}.

        Here callable is a function with two arguments of attribute name and
        value. It should return true of false.

        Also gives the option to strip tags instead of encoding.

        :arg dict token: token to sanitize

        :returns: token or list of tokens

        """

    def sanitize_characters(self, token: _Token) -> _Token | list[_Token]:
        """Handles Characters tokens

        Our overridden tokenizer doesn't do anything with entities. However,
        that means that the serializer will convert all ``&`` in Characters
        tokens to ``&amp;``.

        Since we don't want that, we extract entities here and convert them to
        Entity tokens so the serializer will let them be.

        :arg token: the Characters token to work on

        :returns: a list of tokens

        """

    def sanitize_uri_value(self, value: str, allowed_protocols: Container[str]) -> str | None:
        """Checks a uri value to see if it's allowed

        :arg value: the uri value to sanitize
        :arg allowed_protocols: list of allowed protocols

        :returns: allowed value or None

        """

    def allow_token(self, token: _Token) -> _Token:
        """Handles the case where we're allowing the tag"""

    def disallowed_token(self, token: _Token) -> _Token: ...
