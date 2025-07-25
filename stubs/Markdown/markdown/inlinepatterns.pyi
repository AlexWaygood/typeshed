"""
In version 3.0, a new, more flexible inline processor was added, [`markdown.inlinepatterns.InlineProcessor`][].   The
original inline patterns, which inherit from [`markdown.inlinepatterns.Pattern`][] or one of its children are still
supported, though users are encouraged to migrate.

The new `InlineProcessor` provides two major enhancements to `Patterns`:

1. Inline Processors no longer need to match the entire block, so regular expressions no longer need to start with
  `r'^(.*?)'` and end with `r'(.*?)%'`. This runs faster. The returned [`Match`][re.Match] object will only contain
   what is explicitly matched in the pattern, and extension pattern groups now start with `m.group(1)`.

2.  The `handleMatch` method now takes an additional input called `data`, which is the entire block under analysis,
    not just what is matched with the specified pattern. The method now returns the element *and* the indexes relative
    to `data` that the return element is replacing (usually `m.start(0)` and `m.end(0)`).  If the boundaries are
    returned as `None`, it is assumed that the match did not take place, and nothing will be altered in `data`.

    This allows handling of more complex constructs than regular expressions can handle, e.g., matching nested
    brackets, and explicit control of the span "consumed" by the processor.

"""

import re
from collections.abc import Collection
from typing import ClassVar, NamedTuple
from xml.etree.ElementTree import Element

from markdown import util
from markdown.core import Markdown

def build_inlinepatterns(md: Markdown, **kwargs) -> util.Registry[Pattern]:
    """
    Build the default set of inline patterns for Markdown.

    The order in which processors and/or patterns are applied is very important - e.g. if we first replace
    `http://.../` links with `<a>` tags and _then_ try to replace inline HTML, we would end up with a mess. So, we
    apply the expressions in the following order:

    * backticks and escaped characters have to be handled before everything else so that we can preempt any markdown
      patterns by escaping them;

    * then we handle the various types of links (auto-links must be handled before inline HTML);

    * then we handle inline HTML.  At this point we will simply replace all inline HTML strings with a placeholder
      and add the actual HTML to a stash;

    * finally we apply strong, emphasis, etc.

    """

NOIMG: str
BACKTICK_RE: str
ESCAPE_RE: str
EMPHASIS_RE: str
STRONG_RE: str
SMART_STRONG_RE: str
SMART_EMPHASIS_RE: str
SMART_STRONG_EM_RE: str
EM_STRONG_RE: str
EM_STRONG2_RE: str
STRONG_EM_RE: str
STRONG_EM2_RE: str
STRONG_EM3_RE: str
LINK_RE: str
IMAGE_LINK_RE: str
REFERENCE_RE: str
IMAGE_REFERENCE_RE: str
NOT_STRONG_RE: str
AUTOLINK_RE: str
AUTOMAIL_RE: str
HTML_RE: str
ENTITY_RE: str
LINE_BREAK_RE: str

def dequote(string: str) -> str:
    """Remove quotes from around a string."""

class EmStrongItem(NamedTuple):
    """Emphasis/strong pattern item."""

    pattern: re.Pattern[str]
    builder: str
    tags: str

class Pattern:
    """
    Base class that inline patterns subclass.

    Inline patterns are handled by means of `Pattern` subclasses, one per regular expression.
    Each pattern object uses a single regular expression and must support the following methods:
    [`getCompiledRegExp`][markdown.inlinepatterns.Pattern.getCompiledRegExp] and
    [`handleMatch`][markdown.inlinepatterns.Pattern.handleMatch].

    All the regular expressions used by `Pattern` subclasses must capture the whole block.  For this
    reason, they all start with `^(.*)` and end with `(.*)!`.  When passing a regular expression on
    class initialization, the `^(.*)` and `(.*)!` are added automatically and the regular expression
    is pre-compiled.

    It is strongly suggested that the newer style [`markdown.inlinepatterns.InlineProcessor`][] that
    use a more efficient and flexible search approach be used instead. However, the older style
    `Pattern` remains for backward compatibility with many existing third-party extensions.

    """

    ANCESTOR_EXCLUDES: ClassVar[Collection[str]]
    pattern: str
    compiled_re: re.Pattern[str]
    md: Markdown
    def __init__(self, pattern: str, md: Markdown | None = None) -> None:
        """
        Create an instant of an inline pattern.

        Arguments:
            pattern: A regular expression that matches a pattern.
            md: An optional pointer to the instance of `markdown.Markdown` and is available as
                `self.md` on the class instance.


        """

    def getCompiledRegExp(self) -> re.Pattern[str]:
        """Return a compiled regular expression."""

    def handleMatch(self, m: re.Match[str]) -> str | Element | None:
        """Return a ElementTree element from the given match.

        Subclasses should override this method.

        Arguments:
            m: A match object containing a match of the pattern.

        Returns: An ElementTree Element object.

        """

    def type(self) -> str:
        """Return class name, to define pattern type"""

    def unescape(self, text: str) -> str:
        """Return unescaped text given text with an inline placeholder."""

class InlineProcessor(Pattern):
    """
    Base class that inline processors subclass.

    This is the newer style inline processor that uses a more
    efficient and flexible search approach.

    """

    safe_mode: bool
    def __init__(self, pattern: str, md: Markdown | None = None) -> None:
        """
        Create an instant of an inline processor.

        Arguments:
            pattern: A regular expression that matches a pattern.
            md: An optional pointer to the instance of `markdown.Markdown` and is available as
                `self.md` on the class instance.

        """

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[Element | str | None, int | None, int | None]:  # type: ignore[override]
        """Return a ElementTree element from the given match and the
        start and end index of the matched text.

        If `start` and/or `end` are returned as `None`, it will be
        assumed that the processor did not find a valid region of text.

        Subclasses should override this method.

        Arguments:
            m: A re match object containing a match of the pattern.
            data: The buffer currently under analysis.

        Returns:
            el: The ElementTree element, text or None.
            start: The start of the region that has been matched or None.
            end: The end of the region that has been matched or None.

        """

class SimpleTextPattern(Pattern):
    """Return a simple text of `group(2)` of a Pattern."""

class SimpleTextInlineProcessor(InlineProcessor):
    """Return a simple text of `group(1)` of a Pattern."""

class EscapeInlineProcessor(InlineProcessor):
    """Return an escaped character."""

class SimpleTagPattern(Pattern):
    """
    Return element of type `tag` with a text attribute of `group(3)`
    of a Pattern.

    """

    tag: str
    def __init__(self, pattern: str, tag: str) -> None:
        """
        Create an instant of an simple tag pattern.

        Arguments:
            pattern: A regular expression that matches a pattern.
            tag: Tag of element.

        """

class SimpleTagInlineProcessor(InlineProcessor):
    """
    Return element of type `tag` with a text attribute of `group(2)`
    of a Pattern.

    """

    tag: str
    def __init__(self, pattern: str, tag: str) -> None:
        """
        Create an instant of an simple tag processor.

        Arguments:
            pattern: A regular expression that matches a pattern.
            tag: Tag of element.

        """

class SubstituteTagPattern(SimpleTagPattern):
    """Return an element of type `tag` with no children."""

class SubstituteTagInlineProcessor(SimpleTagInlineProcessor):
    """Return an element of type `tag` with no children."""

class BacktickInlineProcessor(InlineProcessor):
    """Return a `<code>` element containing the escaped matching text."""

    ESCAPED_BSLASH: str
    tag: str
    def __init__(self, pattern: str) -> None: ...

class DoubleTagPattern(SimpleTagPattern):
    """Return a ElementTree element nested in tag2 nested in tag1.

    Useful for strong emphasis etc.

    """

class DoubleTagInlineProcessor(SimpleTagInlineProcessor):
    """Return a ElementTree element nested in tag2 nested in tag1.

    Useful for strong emphasis etc.

    """

class HtmlInlineProcessor(InlineProcessor):
    """Store raw inline html and return a placeholder."""

    def unescape(self, text: str) -> str:
        """Return unescaped text given text with an inline placeholder."""

    def backslash_unescape(self, text: str) -> str:
        """Return text with backslash escapes undone (backslashes are restored)."""

class AsteriskProcessor(InlineProcessor):
    """Emphasis processor for handling strong and em matches inside asterisks."""

    PATTERNS: ClassVar[list[EmStrongItem]]
    def build_single(self, m: re.Match[str], tag: str, idx: int) -> Element:
        """Return single tag."""

    def build_double(self, m: re.Match[str], tags: str, idx: int) -> Element:
        """Return double tag."""

    def build_double2(self, m: re.Match[str], tags: str, idx: int) -> Element:
        """Return double tags (variant 2): `<strong>text <em>text</em></strong>`."""

    def parse_sub_patterns(self, data: str, parent: Element, last: Element | None, idx: int) -> None:
        """
        Parses sub patterns.

        `data`: text to evaluate.

        `parent`: Parent to attach text and sub elements to.

        `last`: Last appended child to parent. Can also be None if parent has no children.

        `idx`: Current pattern index that was used to evaluate the parent.
        """

    def build_element(self, m: re.Match[str], builder: str, tags: str, index: int) -> Element:
        """Element builder."""

class UnderscoreProcessor(AsteriskProcessor):
    """Emphasis processor for handling strong and em matches inside underscores."""

class LinkInlineProcessor(InlineProcessor):
    """Return a link element from the given match."""

    RE_LINK: ClassVar[re.Pattern[str]]
    RE_TITLE_CLEAN: ClassVar[re.Pattern[str]]
    def getLink(self, data: str, index: int) -> tuple[str, str | None, int, bool]:
        """Parse data between `()` of `[Text]()` allowing recursive `()`."""

    def getText(self, data: str, index: int) -> tuple[str, int, bool]:
        """Parse the content between `[]` of the start of an image or link
        resolving nested square brackets.

        """

class ImageInlineProcessor(LinkInlineProcessor):
    """Return a `img` element from the given match."""

class ReferenceInlineProcessor(LinkInlineProcessor):
    """Match to a stored reference and return link element."""

    NEWLINE_CLEANUP_RE: ClassVar[re.Pattern[str]]
    def evalId(self, data: str, index: int, text: str) -> tuple[str | None, int, bool]:
        """
        Evaluate the id portion of `[ref][id]`.

        If `[ref][]` use `[ref]`.
        """

    def makeTag(self, href: str, title: str, text: str) -> Element:
        """Return an `a` [`Element`][xml.etree.ElementTree.Element]."""

class ShortReferenceInlineProcessor(ReferenceInlineProcessor):
    """Short form of reference: `[google]`."""

class ImageReferenceInlineProcessor(ReferenceInlineProcessor):
    """Match to a stored reference and return `img` element."""

class ShortImageReferenceInlineProcessor(ImageReferenceInlineProcessor):
    """Short form of image reference: `![ref]`."""

class AutolinkInlineProcessor(InlineProcessor):
    """Return a link Element given an auto-link (`<http://example/com>`)."""

class AutomailInlineProcessor(InlineProcessor):
    """
    Return a `mailto` link Element given an auto-mail link (`<foo@example.com>`).
    """
