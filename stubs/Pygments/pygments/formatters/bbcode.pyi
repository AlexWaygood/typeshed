"""
pygments.formatters.bbcode
~~~~~~~~~~~~~~~~~~~~~~~~~~

BBcode formatter.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any, TypeVar

from pygments.formatter import Formatter

_T = TypeVar("_T", str, bytes)

class BBCodeFormatter(Formatter[_T]):
    """
    Format tokens with BBcodes. These formatting codes are used by many
    bulletin boards, so you can highlight your sourcecode with pygments before
    posting it there.

    This formatter has no support for background colors and borders, as there
    are no common BBcode tags for that.

    Some board systems (e.g. phpBB) don't support colors in their [code] tag,
    so you can't use the highlighting together with that tag.
    Text in a [code] tag usually is shown with a monospace font (which this
    formatter can do with the ``monofont`` option) and no spaces (which you
    need for indentation) are removed.

    Additional options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `codetag`
        If set to true, put the output into ``[code]`` tags (default:
        ``false``)

    `monofont`
        If set to true, add a tag to show the code with a monospace font
        (default: ``false``).
    """

    name: str
    aliases: Any
    filenames: Any
    styles: Any
    def format_unencoded(self, tokensource, outfile) -> None: ...
