"""authlib.oauth2.rfc6749.resource_protector.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implementation of Accessing Protected Resources per `Section 7`_.

.. _`Section 7`: https://tools.ietf.org/html/rfc6749#section-7
"""

from _typeshed import Incomplete

class TokenValidator:
    """Base token validator class. Subclass this validator to register
    into ResourceProtector instance.
    """

    TOKEN_TYPE: str
    realm: Incomplete
    extra_attributes: Incomplete
    def __init__(self, realm=None, **extra_attributes) -> None: ...
    @staticmethod
    def scope_insufficient(token_scopes, required_scopes): ...
    def authenticate_token(self, token_string) -> None:
        """A method to query token from database with the given token string.
        Developers MUST re-implement this method. For instance::

            def authenticate_token(self, token_string):
                return get_token_from_database(token_string)

        :param token_string: A string to represent the access_token.
        :return: token
        """

    def validate_request(self, request) -> None:
        """A method to validate if the HTTP request is valid or not. Developers MUST
        re-implement this method.  For instance, your server requires a
        "X-Device-Version" in the header::

            def validate_request(self, request):
                if "X-Device-Version" not in request.headers:
                    raise InvalidRequestError()

        Usually, you don't have to detect if the request is valid or not. If you have
        to, you MUST re-implement this method.

        :param request: instance of HttpRequest
        :raise: InvalidRequestError
        """

    def validate_token(self, token, scopes, request) -> None:
        """A method to validate if the authorized token is valid, if it has the
        permission on the given scopes. Developers MUST re-implement this method.
        e.g, check if token is expired, revoked::

            def validate_token(self, token, scopes, request):
                if not token:
                    raise InvalidTokenError()
                if token.is_expired() or token.is_revoked():
                    raise InvalidTokenError()
                if not match_token_scopes(token, scopes):
                    raise InsufficientScopeError()
        """

class ResourceProtector:
    def __init__(self) -> None: ...
    def register_token_validator(self, validator: TokenValidator):
        """Register a token validator for a given Authorization type.
        Authlib has a built-in BearerTokenValidator per rfc6750.
        """

    def get_token_validator(self, token_type):
        """Get token validator from registry for the given token type."""

    def parse_request_authorization(self, request):
        """Parse the token and token validator from request Authorization header.
        Here is an example of Authorization header::

            Authorization: Bearer a-token-string

        This method will parse this header, if it can find the validator for
        ``Bearer``, it will return the validator and ``a-token-string``.

        :return: validator, token_string
        :raise: MissingAuthorizationError
        :raise: UnsupportedTokenTypeError
        """

    def validate_request(self, scopes, request, **kwargs):
        """Validate the request and return a token."""
