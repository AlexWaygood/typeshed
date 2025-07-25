"""
A Python-Markdown extension to treat newlines as hard breaks.
Similar to GitHub-flavored Markdown's behavior.

See the [documentation](https://Python-Markdown.github.io/extensions/nl2br)
for details.
"""

from markdown.extensions import Extension

BR_RE: str

class Nl2BrExtension(Extension): ...

def makeExtension(**kwargs) -> Nl2BrExtension: ...
