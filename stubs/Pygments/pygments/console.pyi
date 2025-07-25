"""
pygments.console
~~~~~~~~~~~~~~~~

Format colored console output.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any

esc: str
codes: Any
dark_colors: Any
light_colors: Any

def reset_color(): ...
def colorize(color_key, text): ...
def ansiformat(attr, text):
    """
    Format ``text`` with a color and/or some attributes::

        color       normal color
        *color*     bold color
        _color_     underlined color
        +color+     blinking color
    """
