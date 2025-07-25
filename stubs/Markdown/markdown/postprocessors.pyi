"""

Post-processors run on the text of the entire document after is has been serialized into a string.
Postprocessors should be used to work with the text just before output. Usually, they are used add
back sections that were extracted in a preprocessor, fix up outgoing encodings, or wrap the whole
document.

"""

import re
from typing import ClassVar
from typing_extensions import deprecated

from markdown.core import Markdown

from . import util

def build_postprocessors(md: Markdown, **kwargs) -> util.Registry[Postprocessor]:
    """Build the default postprocessors for Markdown."""

class Postprocessor(util.Processor):
    """
    Postprocessors are run after the ElementTree it converted back into text.

    Each Postprocessor implements a `run` method that takes a pointer to a
    text string, modifies it as necessary and returns a text string.

    Postprocessors must extend `Postprocessor`.

    """

    def run(self, text: str) -> str:
        """
        Subclasses of `Postprocessor` should implement a `run` method, which
        takes the html document as a single text string and returns a
        (possibly modified) string.

        """

class RawHtmlPostprocessor(Postprocessor):
    """Restore raw html to the document."""

    BLOCK_LEVEL_REGEX: ClassVar[re.Pattern[str]]
    def isblocklevel(self, html: str) -> bool:
        """Check is block of HTML is block-level."""

    def stash_to_string(self, text: str) -> str:
        """Convert a stashed object to a string."""

class AndSubstitutePostprocessor(Postprocessor):
    """Restore valid entities"""

@deprecated(
    "This class is deprecated and will be removed in the future; "
    "use [`UnescapeTreeprocessor`][markdown.treeprocessors.UnescapeTreeprocessor] instead."
)
class UnescapePostprocessor(Postprocessor):
    """Restore escaped chars."""

    RE: ClassVar[re.Pattern[str]]
    def unescape(self, m: re.Match[str]) -> str: ...
