from _typeshed import Incomplete
from logging import Logger

from oauthlib.common import Request
from oauthlib.oauth2.rfc6749.request_validator import RequestValidator as OAuth2RequestValidator

log: Logger

class Dispatcher:
    default_grant: Incomplete | None
    oidc_grant: Incomplete | None

class AuthorizationCodeGrantDispatcher(Dispatcher):
    """
    This is an adapter class that will route simple Authorization Code
    requests, those that have `response_type=code` and a scope including
    `openid` to either the `default_grant` or the `oidc_grant` based on
    the scopes requested.
    """

    default_grant: Incomplete | None
    oidc_grant: Incomplete | None
    def __init__(self, default_grant=None, oidc_grant=None) -> None: ...
    def create_authorization_response(self, request: Request, token_handler):
        """Read scope and route to the designated handler."""

    def validate_authorization_request(self, request: Request):
        """Read scope and route to the designated handler."""

class ImplicitTokenGrantDispatcher(Dispatcher):
    """
    This is an adapter class that will route simple Authorization
    requests, those that have `id_token` in `response_type` and a scope
    including `openid` to either the `default_grant` or the `oidc_grant`
    based on the scopes requested.
    """

    default_grant: Incomplete | None
    oidc_grant: Incomplete | None
    def __init__(self, default_grant=None, oidc_grant=None) -> None: ...
    def create_authorization_response(self, request: Request, token_handler):
        """Read scope and route to the designated handler."""

    def validate_authorization_request(self, request: Request):
        """Read scope and route to the designated handler."""

class AuthorizationTokenGrantDispatcher(Dispatcher):
    """
    This is an adapter class that will route simple Token requests, those that authorization_code have a scope
    including 'openid' to either the default_grant or the oidc_grant based on the scopes requested.
    """

    default_grant: Incomplete | None
    oidc_grant: Incomplete | None
    request_validator: OAuth2RequestValidator
    def __init__(self, request_validator: OAuth2RequestValidator, default_grant=None, oidc_grant=None) -> None: ...
    def create_token_response(self, request: Request, token_handler):
        """Read scope and route to the designated handler."""
