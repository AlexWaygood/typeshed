"""
oauthlib.oauth2.rfc6749.errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error used both by OAuth 2 clients and providers to represent the spec
defined error responses for all four core grant types.
"""

from _typeshed import Incomplete
from typing import Any, NoReturn

from oauthlib.common import Request

class OAuth2Error(Exception):
    error: str | None
    status_code: int
    description: str
    uri: str | None
    state: str | None
    redirect_uri: str | None
    client_id: str | None
    scopes: Any
    response_type: str | None
    response_mode: str | None
    grant_type: str | None
    def __init__(
        self,
        description: str | None = None,
        uri: str | None = None,
        state: str | None = None,
        status_code: int | None = None,
        request: Request | None = None,
    ) -> None:
        """
        :param description: A human-readable ASCII [USASCII] text providing
                            additional information, used to assist the client
                            developer in understanding the error that occurred.
                            Values for the "error_description" parameter
                            MUST NOT include characters outside the set
                            x20-21 / x23-5B / x5D-7E.

        :param uri: A URI identifying a human-readable web page with information
                    about the error, used to provide the client developer with
                    additional information about the error.  Values for the
                    "error_uri" parameter MUST conform to the URI- Reference
                    syntax, and thus MUST NOT include characters outside the set
                    x21 / x23-5B / x5D-7E.

        :param state: A CSRF protection value received from the client.

        :param status_code:

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def in_uri(self, uri: str) -> str: ...
    @property
    def twotuples(self) -> list[tuple[str, str | None]]: ...
    @property
    def urlencoded(self) -> str: ...
    @property
    def json(self) -> str: ...
    @property
    def headers(self) -> dict[str, str]: ...

class TokenExpiredError(OAuth2Error):
    error: str

class InsecureTransportError(OAuth2Error):
    error: str
    description: str

class MismatchingStateError(OAuth2Error):
    error: str
    description: str

class MissingCodeError(OAuth2Error):
    error: str

class MissingTokenError(OAuth2Error):
    error: str

class MissingTokenTypeError(OAuth2Error):
    error: str

class FatalClientError(OAuth2Error):
    """
    Errors during authorization where user should not be redirected back.

    If the request fails due to a missing, invalid, or mismatching
    redirection URI, or if the client identifier is missing or invalid,
    the authorization server SHOULD inform the resource owner of the
    error and MUST NOT automatically redirect the user-agent to the
    invalid redirection URI.

    Instead the user should be informed of the error by the provider itself.
    """

class InvalidRequestFatalError(FatalClientError):
    """
    For fatal errors, the request is missing a required parameter, includes
    an invalid parameter value, includes a parameter more than once, or is
    otherwise malformed.
    """

    error: str

class InvalidRedirectURIError(InvalidRequestFatalError):
    description: str

class MissingRedirectURIError(InvalidRequestFatalError):
    description: str

class MismatchingRedirectURIError(InvalidRequestFatalError):
    description: str

class InvalidClientIdError(InvalidRequestFatalError):
    description: str

class MissingClientIdError(InvalidRequestFatalError):
    description: str

class InvalidRequestError(OAuth2Error):
    """
    The request is missing a required parameter, includes an invalid
    parameter value, includes a parameter more than once, or is
    otherwise malformed.
    """

    error: str

class MissingResponseTypeError(InvalidRequestError):
    description: str

class MissingCodeChallengeError(InvalidRequestError):
    """
    If the server requires Proof Key for Code Exchange (PKCE) by OAuth
    public clients and the client does not send the "code_challenge" in
    the request, the authorization endpoint MUST return the authorization
    error response with the "error" value set to "invalid_request".  The
    "error_description" or the response of "error_uri" SHOULD explain the
    nature of error, e.g., code challenge required.
    """

    description: str

class MissingCodeVerifierError(InvalidRequestError):
    """
    The request to the token endpoint, when PKCE is enabled, has
    the parameter `code_verifier` REQUIRED.
    """

    description: str

class AccessDeniedError(OAuth2Error):
    """
    The resource owner or authorization server denied the request.
    """

    error: str

class UnsupportedResponseTypeError(OAuth2Error):
    """
    The authorization server does not support obtaining an authorization
    code using this method.
    """

    error: str

class UnsupportedCodeChallengeMethodError(InvalidRequestError):
    """
    If the server supporting PKCE does not support the requested
    transformation, the authorization endpoint MUST return the
    authorization error response with "error" value set to
    "invalid_request".  The "error_description" or the response of
    "error_uri" SHOULD explain the nature of error, e.g., transform
    algorithm not supported.
    """

    description: str

class InvalidScopeError(OAuth2Error):
    """
    The requested scope is invalid, unknown, or malformed, or
    exceeds the scope granted by the resource owner.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """

    error: str

class ServerError(OAuth2Error):
    """
    The authorization server encountered an unexpected condition that
    prevented it from fulfilling the request.  (This error code is needed
    because a 500 Internal Server Error HTTP status code cannot be returned
    to the client via a HTTP redirect.)
    """

    error: str

class TemporarilyUnavailableError(OAuth2Error):
    """
    The authorization server is currently unable to handle the request
    due to a temporary overloading or maintenance of the server.
    (This error code is needed because a 503 Service Unavailable HTTP
    status code cannot be returned to the client via a HTTP redirect.)
    """

    error: str

class InvalidClientError(FatalClientError):
    """
    Client authentication failed (e.g. unknown client, no client
    authentication included, or unsupported authentication method).
    The authorization server MAY return an HTTP 401 (Unauthorized) status
    code to indicate which HTTP authentication schemes are supported.
    If the client attempted to authenticate via the "Authorization" request
    header field, the authorization server MUST respond with an
    HTTP 401 (Unauthorized) status code, and include the "WWW-Authenticate"
    response header field matching the authentication scheme used by the
    client.
    """

    error: str
    status_code: int

class InvalidGrantError(OAuth2Error):
    """
    The provided authorization grant (e.g. authorization code, resource
    owner credentials) or refresh token is invalid, expired, revoked, does
    not match the redirection URI used in the authorization request, or was
    issued to another client.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """

    error: str
    status_code: int

class UnauthorizedClientError(OAuth2Error):
    """
    The authenticated client is not authorized to use this authorization
    grant type.
    """

    error: str

class UnsupportedGrantTypeError(OAuth2Error):
    """
    The authorization grant type is not supported by the authorization
    server.
    """

    error: str

class UnsupportedTokenTypeError(OAuth2Error):
    """
    The authorization server does not support the hint of the
    presented token type.  I.e. the client tried to revoke an access token
    on a server not supporting this feature.
    """

    error: str

class InvalidTokenError(OAuth2Error):
    """
    The access token provided is expired, revoked, malformed, or
    invalid for other reasons.  The resource SHOULD respond with
    the HTTP 401 (Unauthorized) status code.  The client MAY
    request a new access token and retry the protected resource
    request.
    """

    error: str
    status_code: int
    description: str

class InsufficientScopeError(OAuth2Error):
    """
    The request requires higher privileges than provided by the
    access token.  The resource server SHOULD respond with the HTTP
    403 (Forbidden) status code and MAY include the "scope"
    attribute with the scope necessary to access the protected
    resource.
    """

    error: str
    status_code: int
    description: str

class ConsentRequired(OAuth2Error):
    """
    The Authorization Server requires End-User consent.

    This error MAY be returned when the prompt parameter value in the
    Authentication Request is none, but the Authentication Request cannot be
    completed without displaying a user interface for End-User consent.
    """

    error: str

class LoginRequired(OAuth2Error):
    """
    The Authorization Server requires End-User authentication.

    This error MAY be returned when the prompt parameter value in the
    Authentication Request is none, but the Authentication Request cannot be
    completed without displaying a user interface for End-User authentication.
    """

    error: str

class CustomOAuth2Error(OAuth2Error):
    """
    This error is a placeholder for all custom errors not described by the RFC.
    Some of the popular OAuth2 providers are using custom errors.
    """

    def __init__(
        self,
        error: str,
        description: str | None = None,
        uri: str | None = None,
        state: str | None = None,
        status_code: int | None = None,
        request: Request | None = None,
    ) -> None: ...

def raise_from_error(error: str, params: dict[str, Incomplete] | None = None) -> NoReturn: ...
