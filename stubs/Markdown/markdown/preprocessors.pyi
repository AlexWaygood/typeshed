"""
Preprocessors work on source text before it is broken down into its individual parts.
This is an excellent place to clean up bad characters or to extract portions for later
processing that the parser may otherwise choke on.
"""

from markdown.core import Markdown

from . import util

def build_preprocessors(md: Markdown, **kwargs) -> util.Registry[Preprocessor]:
    """Build and return the default set of preprocessors used by Markdown."""

class Preprocessor(util.Processor):
    """
    Preprocessors are run after the text is broken into lines.

    Each preprocessor implements a `run` method that takes a pointer to a
    list of lines of the document, modifies it as necessary and returns
    either the same pointer or a pointer to a new list.

    Preprocessors must extend `Preprocessor`.

    """

    def run(self, lines: list[str]) -> list[str]:
        """
        Each subclass of `Preprocessor` should override the `run` method, which
        takes the document as a list of strings split by newlines and returns
        the (possibly modified) list of lines.

        """

class NormalizeWhitespace(Preprocessor):
    """Normalize whitespace for consistent parsing."""

class HtmlBlockPreprocessor(Preprocessor):
    """
    Remove html blocks from the text and store them for later retrieval.

    The raw HTML is stored in the [`htmlStash`][markdown.util.HtmlStash] of the
    [`Markdown`][markdown.Markdown] instance.
    """
