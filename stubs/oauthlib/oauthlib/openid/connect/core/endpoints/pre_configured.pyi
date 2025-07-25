"""
oauthlib.openid.connect.core.endpoints.pre_configured
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various endpoints needed
for providing OpenID Connect servers.
"""

from _typeshed import Unused
from collections.abc import Callable

from oauthlib.common import Request
from oauthlib.oauth2.rfc6749.endpoints import (
    AuthorizationEndpoint,
    IntrospectEndpoint,
    ResourceEndpoint,
    RevocationEndpoint,
    TokenEndpoint,
)
from oauthlib.oauth2.rfc6749.grant_types import (
    AuthorizationCodeGrant as OAuth2AuthorizationCodeGrant,
    ClientCredentialsGrant,
    ImplicitGrant as OAuth2ImplicitGrant,
    RefreshTokenGrant,
    ResourceOwnerPasswordCredentialsGrant,
)
from oauthlib.oauth2.rfc6749.request_validator import RequestValidator as OAuth2RequestValidator
from oauthlib.oauth2.rfc6749.tokens import BearerToken
from oauthlib.oauth2.rfc8628.grant_types import DeviceCodeGrant

from ..grant_types import AuthorizationCodeGrant, HybridGrant, ImplicitGrant
from ..grant_types.dispatchers import (
    AuthorizationCodeGrantDispatcher,
    AuthorizationTokenGrantDispatcher,
    ImplicitTokenGrantDispatcher,
)
from ..tokens import JWTToken
from .userinfo import UserInfoEndpoint

class Server(AuthorizationEndpoint, IntrospectEndpoint, TokenEndpoint, ResourceEndpoint, RevocationEndpoint, UserInfoEndpoint):
    """
    An all-in-one endpoint featuring all four major grant types
    and extension grants.
    """

    auth_grant: OAuth2AuthorizationCodeGrant
    implicit_grant: OAuth2ImplicitGrant
    password_grant: ResourceOwnerPasswordCredentialsGrant
    credentials_grant: ClientCredentialsGrant
    refresh_grant: RefreshTokenGrant
    openid_connect_auth: AuthorizationCodeGrant
    openid_connect_implicit: ImplicitGrant
    openid_connect_hybrid: HybridGrant
    device_code_grant: DeviceCodeGrant
    bearer: BearerToken
    jwt: JWTToken
    auth_grant_choice: AuthorizationCodeGrantDispatcher
    implicit_grant_choice: ImplicitTokenGrantDispatcher
    token_grant_choice: AuthorizationTokenGrantDispatcher
    def __init__(
        self,
        request_validator: OAuth2RequestValidator,
        token_expires_in: int | Callable[[Request], int] | None = None,
        token_generator: Callable[[Request], str] | None = None,
        refresh_token_generator: Callable[[Request], str] | None = None,
        *args: Unused,
    ) -> None:
        """Construct a new all-grants-in-one server.

        :param request_validator: An implementation of
                                  oauthlib.oauth2.RequestValidator.
        :param token_expires_in: An int or a function to generate a token
                                 expiration offset (in seconds) given a
                                 oauthlib.common.Request object.
        :param token_generator: A function to generate a token from a request.
        :param refresh_token_generator: A function to generate a token from a
                                        request for the refresh token.
        :param kwargs: Extra parameters to pass to authorization-,
                       token-, resource-, and revocation-endpoint constructors.
        """
