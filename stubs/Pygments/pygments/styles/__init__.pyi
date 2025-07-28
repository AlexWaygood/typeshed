"""
pygments.styles
~~~~~~~~~~~~~~~

Contains built-in styles.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from collections.abc import Iterator, Mapping

from pygments.style import Style
from pygments.util import ClassNotFound as ClassNotFound

STYLE_MAP: Mapping[str, str]

def get_style_by_name(name) -> type[Style]:
    """
    Return a style class by its short name. The names of the builtin styles
    are listed in :data:`pygments.styles.STYLE_MAP`.

    Will raise :exc:`pygments.util.ClassNotFound` if no style of that name is
    found.
    """

def get_all_styles() -> Iterator[str]:
    """Return a generator for all styles by name, both builtin and plugin."""

# Having every style class here doesn't seem to be worth it
def __getattr__(name: str): ...  # incomplete module
