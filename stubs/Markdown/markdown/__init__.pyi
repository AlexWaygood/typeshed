"""
Python-Markdown provides two public functions ([`markdown.markdown`][] and [`markdown.markdownFromFile`][])
both of which wrap the public class [`markdown.Markdown`][]. All submodules support these public functions
and class and/or provide extension support.

Modules:
    core: Core functionality.
    preprocessors: Pre-processors.
    blockparser: Core Markdown block parser.
    blockprocessors: Block processors.
    treeprocessors: Tree processors.
    inlinepatterns: Inline patterns.
    postprocessors: Post-processors.
    serializers: Serializers.
    util: Utility functions.
    htmlparser: HTML parser.
    test_tools: Testing utilities.
    extensions: Markdown extensions.
"""

from .__meta__ import __version__ as __version__, __version_info__ as __version_info__
from .core import Markdown as Markdown, markdown as markdown, markdownFromFile as markdownFromFile
from .extensions import Extension as Extension

__all__ = ["Markdown", "markdown", "markdownFromFile"]
