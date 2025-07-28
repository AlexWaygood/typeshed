from collections.abc import Container, Iterable
from typing_extensions import TypeAlias

from .callbacks import _Callback
from .css_sanitizer import CSSSanitizer
from .linkifier import DEFAULT_CALLBACKS as DEFAULT_CALLBACKS, Linker as Linker
from .sanitizer import (
    ALLOWED_ATTRIBUTES as ALLOWED_ATTRIBUTES,
    ALLOWED_PROTOCOLS as ALLOWED_PROTOCOLS,
    ALLOWED_TAGS as ALLOWED_TAGS,
    Cleaner as Cleaner,
    _Attributes,
)

__all__ = ["clean", "linkify"]

__releasedate__: str
__version__: str

_HTMLAttrKey: TypeAlias = tuple[str | None, str]  # noqa: Y047

def clean(
    text: str,
    tags: Iterable[str] = ...,
    attributes: _Attributes = ...,
    protocols: Iterable[str] = ...,
    strip: bool = False,
    strip_comments: bool = True,
    css_sanitizer: CSSSanitizer | None = None,
) -> str:
    """Clean an HTML fragment of malicious content and return it

    This function is a security-focused function whose sole purpose is to
    remove malicious content from a string such that it can be displayed as
    content in a web page.

    This function is not designed to use to transform content to be used in
    non-web-page contexts.

    Example::

        import bleach

        better_text = bleach.clean(yucky_text)


    .. Note::

       If you're cleaning a lot of text and passing the same argument values or
       you want more configurability, consider using a
       :py:class:`bleach.sanitizer.Cleaner` instance.

    :arg str text: the text to clean

    :arg set tags: set of allowed tags; defaults to
        ``bleach.sanitizer.ALLOWED_TAGS``

    :arg dict attributes: allowed attributes; can be a callable, list or dict;
        defaults to ``bleach.sanitizer.ALLOWED_ATTRIBUTES``

    :arg list protocols: allowed list of protocols for links; defaults
        to ``bleach.sanitizer.ALLOWED_PROTOCOLS``

    :arg bool strip: whether or not to strip disallowed elements

    :arg bool strip_comments: whether or not to strip HTML comments

    :arg CSSSanitizer css_sanitizer: instance with a "sanitize_css" method for
        sanitizing style attribute values and style text; defaults to None

    :returns: cleaned text as unicode

    """

def linkify(
    text: str, callbacks: Iterable[_Callback] = ..., skip_tags: Container[str] | None = None, parse_email: bool = False
) -> str:
    """Convert URL-like strings in an HTML fragment to links

    This function converts strings that look like URLs, domain names and email
    addresses in text that may be an HTML fragment to links, while preserving:

    1. links already in the string
    2. urls found in attributes
    3. email addresses

    linkify does a best-effort approach and tries to recover from bad
    situations due to crazy text.

    .. Note::

       If you're linking a lot of text and passing the same argument values or
       you want more configurability, consider using a
       :py:class:`bleach.linkifier.Linker` instance.

    .. Note::

       If you have text that you want to clean and then linkify, consider using
       the :py:class:`bleach.linkifier.LinkifyFilter` as a filter in the clean
       pass. That way you're not parsing the HTML twice.

    :arg str text: the text to linkify

    :arg list callbacks: list of callbacks to run when adjusting tag attributes;
        defaults to ``bleach.linkifier.DEFAULT_CALLBACKS``

    :arg list skip_tags: list of tags that you don't want to linkify the
        contents of; for example, you could set this to ``['pre']`` to skip
        linkifying contents of ``pre`` tags

    :arg bool parse_email: whether or not to linkify email addresses

    :returns: linkified text as unicode

    """
