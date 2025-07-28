"""authlib.oauth2.rfc8628.
~~~~~~~~~~~~~~~~~~~~~~

This module represents an implementation of
OAuth 2.0 Device Authorization Grant.

https://tools.ietf.org/html/rfc8628
"""

from .device_code import DEVICE_CODE_GRANT_TYPE as DEVICE_CODE_GRANT_TYPE, DeviceCodeGrant as DeviceCodeGrant
from .endpoint import DeviceAuthorizationEndpoint as DeviceAuthorizationEndpoint
from .errors import (
    AuthorizationPendingError as AuthorizationPendingError,
    ExpiredTokenError as ExpiredTokenError,
    SlowDownError as SlowDownError,
)
from .models import DeviceCredentialDict as DeviceCredentialDict, DeviceCredentialMixin as DeviceCredentialMixin

__all__ = [
    "DeviceAuthorizationEndpoint",
    "DeviceCodeGrant",
    "DEVICE_CODE_GRANT_TYPE",
    "DeviceCredentialMixin",
    "DeviceCredentialDict",
    "AuthorizationPendingError",
    "SlowDownError",
    "ExpiredTokenError",
]
