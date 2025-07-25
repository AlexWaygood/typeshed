"""authlib.oauth1.rfc5849.errors.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RFC5849 has no definition on errors. This module is designed by
Authlib based on OAuth 1.0a `Section 10`_ with some changes.

.. _`Section 10`: https://oauth.net/core/1.0a/#rfc.section.10
"""

from authlib.common.errors import AuthlibHTTPError

class OAuth1Error(AuthlibHTTPError):
    def __init__(self, description=None, uri=None, status_code=None) -> None: ...
    def get_headers(self):
        """Get a list of headers."""

class InsecureTransportError(OAuth1Error):
    error: str
    description: str
    @classmethod
    def check(cls, uri) -> None: ...

class InvalidRequestError(OAuth1Error):
    error: str

class UnsupportedParameterError(OAuth1Error):
    error: str

class UnsupportedSignatureMethodError(OAuth1Error):
    error: str

class MissingRequiredParameterError(OAuth1Error):
    error: str
    def __init__(self, key) -> None: ...

class DuplicatedOAuthProtocolParameterError(OAuth1Error):
    error: str

class InvalidClientError(OAuth1Error):
    error: str
    status_code: int

class InvalidTokenError(OAuth1Error):
    error: str
    description: str
    status_code: int

class InvalidSignatureError(OAuth1Error):
    error: str
    status_code: int

class InvalidNonceError(OAuth1Error):
    error: str
    status_code: int

class AccessDeniedError(OAuth1Error):
    error: str
    description: str

class MethodNotAllowedError(OAuth1Error):
    error: str
    status_code: int
