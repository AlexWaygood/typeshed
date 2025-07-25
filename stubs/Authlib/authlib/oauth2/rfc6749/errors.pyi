"""authlib.oauth2.rfc6749.errors.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implementation for OAuth 2 Error Response. A basic error has
parameters:

Error:
REQUIRED.  A single ASCII [USASCII] error code.

error_description
OPTIONAL.  Human-readable ASCII [USASCII] text providing
additional information, used to assist the client developer in
understanding the error that occurred.

error_uri
OPTIONAL.  A URI identifying a human-readable web page with
information about the error, used to provide the client
developer with additional information about the error.
Values for the "error_uri" parameter MUST conform to the
URI-reference syntax and thus MUST NOT include characters
outside the set %x21 / %x23-5B / %x5D-7E.

state
REQUIRED if a "state" parameter was present in the client
authorization request.  The exact value received from the
client.

https://tools.ietf.org/html/rfc6749#section-5.2

:copyright: (c) 2017 by Hsiaoming Yang.

"""

from _typeshed import Incomplete

from authlib.oauth2 import OAuth2Error as OAuth2Error

__all__ = [
    "OAuth2Error",
    "InsecureTransportError",
    "InvalidRequestError",
    "InvalidClientError",
    "UnauthorizedClientError",
    "InvalidGrantError",
    "UnsupportedResponseTypeError",
    "UnsupportedGrantTypeError",
    "InvalidScopeError",
    "AccessDeniedError",
    "MissingAuthorizationError",
    "UnsupportedTokenTypeError",
    "MissingCodeException",
    "MissingTokenException",
    "MissingTokenTypeException",
    "MismatchingStateException",
]

class InsecureTransportError(OAuth2Error):
    error: str
    description: str
    @classmethod
    def check(cls, uri) -> None:
        """Check and raise InsecureTransportError with the given URI."""

class InvalidRequestError(OAuth2Error):
    """The request is missing a required parameter, includes an
    unsupported parameter value (other than grant type),
    repeats a parameter, includes multiple credentials,
    utilizes more than one mechanism for authenticating the
    client, or is otherwise malformed.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """

    error: str

class InvalidClientError(OAuth2Error):
    """Client authentication failed (e.g., unknown client, no
    client authentication included, or unsupported
    authentication method).  The authorization server MAY
    return an HTTP 401 (Unauthorized) status code to indicate
    which HTTP authentication schemes are supported.  If the
    client attempted to authenticate via the "Authorization"
    request header field, the authorization server MUST
    respond with an HTTP 401 (Unauthorized) status code and
    include the "WWW-Authenticate" response header field
    matching the authentication scheme used by the client.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """

    error: str
    status_code: int
    def get_headers(self): ...

class InvalidGrantError(OAuth2Error):
    """The provided authorization grant (e.g., authorization
    code, resource owner credentials) or refresh token is
    invalid, expired, revoked, does not match the redirection
    URI used in the authorization request, or was issued to
    another client.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """

    error: str

class UnauthorizedClientError(OAuth2Error):
    """The authenticated client is not authorized to use this
    authorization grant type.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """

    error: str

class UnsupportedResponseTypeError(OAuth2Error):
    """The authorization server does not support obtaining
    an access token using this method.
    """

    error: str
    response_type: Incomplete
    def __init__(
        self,
        response_type,
        description=None,
        uri=None,
        status_code=None,
        state=None,
        redirect_uri=None,
        redirect_fragment: bool = False,
        error=None,
    ) -> None: ...
    def get_error_description(self): ...

class UnsupportedGrantTypeError(OAuth2Error):
    """The authorization grant type is not supported by the
    authorization server.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """

    error: str
    grant_type: Incomplete
    def __init__(self, grant_type) -> None: ...
    def get_error_description(self): ...

class InvalidScopeError(OAuth2Error):
    """The requested scope is invalid, unknown, malformed, or
    exceeds the scope granted by the resource owner.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """

    error: str
    description: str

class AccessDeniedError(OAuth2Error):
    """The resource owner or authorization server denied the request.

    Used in authorization endpoint for "code" and "implicit". Defined in
    `Section 4.1.2.1`_.

    .. _`Section 4.1.2.1`: https://tools.ietf.org/html/rfc6749#section-4.1.2.1
    """

    error: str
    description: str

class ForbiddenError(OAuth2Error):
    status_code: int
    auth_type: Incomplete
    realm: Incomplete
    def __init__(self, auth_type=None, realm=None) -> None: ...
    def get_headers(self): ...

class MissingAuthorizationError(ForbiddenError):
    error: str
    description: str

class UnsupportedTokenTypeError(ForbiddenError):
    error: str

class MissingCodeException(OAuth2Error):
    error: str
    description: str

class MissingTokenException(OAuth2Error):
    error: str
    description: str

class MissingTokenTypeException(OAuth2Error):
    error: str
    description: str

class MismatchingStateException(OAuth2Error):
    error: str
    description: str
