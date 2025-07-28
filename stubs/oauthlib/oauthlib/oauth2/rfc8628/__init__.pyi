"""
oauthlib.oauth2.rfc8628
~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for consuming and providing OAuth 2.0 Device Authorization RFC8628.
"""

from logging import Logger

from .errors import (
    AuthorizationPendingError as AuthorizationPendingError,
    ExpiredTokenError as ExpiredTokenError,
    SlowDownError as SlowDownError,
)

log: Logger
