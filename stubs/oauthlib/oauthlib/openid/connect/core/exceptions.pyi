"""
oauthlib.oauth2.rfc6749.errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error used both by OAuth 2 clients and providers to represent the spec
defined error responses for all four core grant types.
"""

from oauthlib.oauth2.rfc6749.errors import FatalClientError, OAuth2Error

class FatalOpenIDClientError(FatalClientError): ...
class OpenIDClientError(OAuth2Error): ...

class InteractionRequired(OpenIDClientError):
    """
    The Authorization Server requires End-User interaction to proceed.

    This error MAY be returned when the prompt parameter value in the
    Authentication Request is none, but the Authentication Request cannot be
    completed without displaying a user interface for End-User interaction.
    """

    error: str
    status_code: int

class LoginRequired(OpenIDClientError):
    """
    The Authorization Server requires End-User authentication.

    This error MAY be returned when the prompt parameter value in the
    Authentication Request is none, but the Authentication Request cannot be
    completed without displaying a user interface for End-User authentication.
    """

    error: str
    status_code: int

class AccountSelectionRequired(OpenIDClientError):
    """
    The End-User is REQUIRED to select a session at the Authorization Server.

    The End-User MAY be authenticated at the Authorization Server with
    different associated accounts, but the End-User did not select a session.
    This error MAY be returned when the prompt parameter value in the
    Authentication Request is none, but the Authentication Request cannot be
    completed without displaying a user interface to prompt for a session to
    use.
    """

    error: str

class ConsentRequired(OpenIDClientError):
    """
    The Authorization Server requires End-User consent.

    This error MAY be returned when the prompt parameter value in the
    Authentication Request is none, but the Authentication Request cannot be
    completed without displaying a user interface for End-User consent.
    """

    error: str
    status_code: int

class InvalidRequestURI(OpenIDClientError):
    """
    The request_uri in the Authorization Request returns an error or
    contains invalid data.
    """

    error: str
    description: str

class InvalidRequestObject(OpenIDClientError):
    """
    The request parameter contains an invalid Request Object.
    """

    error: str
    description: str

class RequestNotSupported(OpenIDClientError):
    """
    The OP does not support use of the request parameter.
    """

    error: str
    description: str

class RequestURINotSupported(OpenIDClientError):
    """
    The OP does not support use of the request_uri parameter.
    """

    error: str
    description: str

class RegistrationNotSupported(OpenIDClientError):
    """
    The OP does not support use of the registration parameter.
    """

    error: str
    description: str

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

def raise_from_error(error: object, params: dict[str, str] | None = None) -> None: ...
