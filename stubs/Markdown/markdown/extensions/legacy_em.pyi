"""
This extension provides legacy behavior for _connected_words_.
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import UnderscoreProcessor

EMPHASIS_RE: str
STRONG_RE: str
STRONG_EM_RE: str

class LegacyUnderscoreProcessor(UnderscoreProcessor):
    """Emphasis processor for handling strong and em matches inside underscores."""

class LegacyEmExtension(Extension):
    """Add legacy_em extension to Markdown class."""

def makeExtension(**kwargs) -> LegacyEmExtension:
    """Return an instance of the `LegacyEmExtension`"""
