"""
oauthlib.oauth2.rfc6749.endpoints.pre_configured
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various endpoints needed
for providing OAuth 2.0 RFC6749 servers.
"""

from _typeshed import Unused
from collections.abc import Callable

from oauthlib.common import Request
from oauthlib.oauth2.rfc8628.grant_types import DeviceCodeGrant

from ..grant_types import (
    AuthorizationCodeGrant,
    ClientCredentialsGrant,
    ImplicitGrant,
    RefreshTokenGrant,
    ResourceOwnerPasswordCredentialsGrant,
)
from ..request_validator import RequestValidator
from ..tokens import BearerToken
from .authorization import AuthorizationEndpoint
from .introspect import IntrospectEndpoint
from .resource import ResourceEndpoint
from .revocation import RevocationEndpoint
from .token import TokenEndpoint

class Server(AuthorizationEndpoint, IntrospectEndpoint, TokenEndpoint, ResourceEndpoint, RevocationEndpoint):
    """
    An all-in-one endpoint featuring all four major grant types
    and extension grants.
    """

    auth_grant: AuthorizationCodeGrant
    implicit_grant: ImplicitGrant
    password_grant: ResourceOwnerPasswordCredentialsGrant
    credentials_grant: ClientCredentialsGrant
    refresh_grant: RefreshTokenGrant
    device_code_grant: DeviceCodeGrant
    bearer: BearerToken
    def __init__(
        self,
        request_validator: RequestValidator,
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

class WebApplicationServer(AuthorizationEndpoint, IntrospectEndpoint, TokenEndpoint, ResourceEndpoint, RevocationEndpoint):
    """An all-in-one endpoint featuring Authorization code grant and Bearer tokens."""

    auth_grant: AuthorizationCodeGrant
    refresh_grant: RefreshTokenGrant
    bearer: BearerToken
    def __init__(
        self,
        request_validator: RequestValidator,
        token_generator: Callable[[Request], str] | None = None,
        token_expires_in: int | Callable[[Request], int] | None = None,
        refresh_token_generator: Callable[[Request], str] | None = None,
    ) -> None:
        """Construct a new web application server.

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

class MobileApplicationServer(AuthorizationEndpoint, IntrospectEndpoint, ResourceEndpoint, RevocationEndpoint):
    """An all-in-one endpoint featuring Implicit code grant and Bearer tokens."""

    implicit_grant: ImplicitGrant
    bearer: BearerToken
    def __init__(
        self,
        request_validator: RequestValidator,
        token_generator: Callable[[Request], str] | None = None,
        token_expires_in: int | Callable[[Request], int] | None = None,
        refresh_token_generator: Callable[[Request], str] | None = None,
    ) -> None:
        """Construct a new implicit grant server.

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

class LegacyApplicationServer(TokenEndpoint, IntrospectEndpoint, ResourceEndpoint, RevocationEndpoint):
    """An all-in-one endpoint featuring Resource Owner Password Credentials grant and Bearer tokens."""

    password_grant: ResourceOwnerPasswordCredentialsGrant
    refresh_grant: RefreshTokenGrant
    bearer: BearerToken
    def __init__(
        self,
        request_validator: RequestValidator,
        token_generator: Callable[[Request], str] | None = None,
        token_expires_in: int | Callable[[Request], int] | None = None,
        refresh_token_generator: Callable[[Request], str] | None = None,
    ) -> None:
        """Construct a resource owner password credentials grant server.

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

class BackendApplicationServer(TokenEndpoint, IntrospectEndpoint, ResourceEndpoint, RevocationEndpoint):
    """An all-in-one endpoint featuring Client Credentials grant and Bearer tokens."""

    credentials_grant: ClientCredentialsGrant
    bearer: BearerToken
    def __init__(
        self,
        request_validator: RequestValidator,
        token_generator: Callable[[Request], str] | None = None,
        token_expires_in: int | Callable[[Request], int] | None = None,
        refresh_token_generator: Callable[[Request], str] | None = None,
    ) -> None:
        """Construct a client credentials grant server.

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
