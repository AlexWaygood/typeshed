"""authlib.oauth2.rfc7591.
~~~~~~~~~~~~~~~~~~~~~~

This module represents a direct implementation of
OAuth 2.0 Dynamic Client Registration Protocol.

https://tools.ietf.org/html/rfc7591
"""

from .claims import ClientMetadataClaims as ClientMetadataClaims
from .endpoint import ClientRegistrationEndpoint as ClientRegistrationEndpoint
from .errors import (
    InvalidClientMetadataError as InvalidClientMetadataError,
    InvalidRedirectURIError as InvalidRedirectURIError,
    InvalidSoftwareStatementError as InvalidSoftwareStatementError,
    UnapprovedSoftwareStatementError as UnapprovedSoftwareStatementError,
)

__all__ = [
    "ClientMetadataClaims",
    "ClientRegistrationEndpoint",
    "InvalidRedirectURIError",
    "InvalidClientMetadataError",
    "InvalidSoftwareStatementError",
    "UnapprovedSoftwareStatementError",
]
