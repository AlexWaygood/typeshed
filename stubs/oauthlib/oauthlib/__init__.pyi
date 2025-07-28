"""
oauthlib
~~~~~~~~

A generic, spec-compliant, thorough implementation of the OAuth
request-signing logic.

:copyright: (c) The OAuthlib Community
:license: BSD-3-Clause, see LICENSE for details.
"""

from typing import Final

__author__: Final[str]
__version__: Final[str]

def set_debug(debug_val: bool) -> None:
    """Set value of debug flag

    :param debug_val: Value to set. Must be a bool value.
    """

def get_debug() -> bool:
    """Get debug mode value.

    :return: `True` if debug mode is on, `False` otherwise
    """
