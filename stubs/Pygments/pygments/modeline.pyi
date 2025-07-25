"""
pygments.modeline
~~~~~~~~~~~~~~~~~

A simple modeline parser (based on pymodeline).

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

def get_filetype_from_buffer(buf, max_lines: int = 5):
    """
    Scan the buffer for modelines and return filetype if one is found.
    """
