"""
oauthlib.oauth2.rfc6749
~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for consuming and providing OAuth 2.0 RFC6749.
"""

from logging import Logger

from .endpoints.base import BaseEndpoint as BaseEndpoint, catch_errors_and_unavailability as catch_errors_and_unavailability
from .errors import (
    FatalClientError as FatalClientError,
    OAuth2Error as OAuth2Error,
    ServerError as ServerError,
    TemporarilyUnavailableError as TemporarilyUnavailableError,
)

log: Logger
