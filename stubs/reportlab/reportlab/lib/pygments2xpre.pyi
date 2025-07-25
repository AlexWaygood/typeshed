"""Helps you output colourised code snippets in ReportLab documents.

Platypus has an 'XPreformatted' flowable for handling preformatted
text, with variations in fonts and colors.   If Pygments is installed,
calling 'pygments2xpre' will return content suitable for display in
an XPreformatted object.  If it's not installed, you won't get colours.

For a list of available lexers see http://pygments.org/docs/

"""

def pygments2xpre(s, language: str = "python"):
    """Return markup suitable for XPreformatted"""

__all__ = ("pygments2xpre",)
