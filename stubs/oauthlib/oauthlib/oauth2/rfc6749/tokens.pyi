"""
oauthlib.oauth2.rfc6749.tokens
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains methods for adding two types of access tokens to requests.

- Bearer https://tools.ietf.org/html/rfc6750
- MAC https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-01
"""

import datetime
from _typeshed import Incomplete
from collections.abc import Callable
from typing import Literal

from oauthlib.common import Request, _HTTPMethod
from oauthlib.oauth2.rfc6749.request_validator import RequestValidator

class OAuth2Token(dict[str, Incomplete]):
    def __init__(
        self, params: dict[str, Incomplete], old_scope: str | set[object] | tuple[object] | list[object] | None = None
    ) -> None: ...
    @property
    def scope_changed(self) -> bool: ...
    @property
    def old_scope(self) -> str | None: ...
    @property
    def old_scopes(self) -> list[str]: ...
    @property
    def scope(self) -> str | None: ...
    @property
    def scopes(self) -> list[str]: ...
    @property
    def missing_scopes(self) -> list[str]: ...
    @property
    def additional_scopes(self) -> list[str]: ...

def prepare_mac_header(
    token: str,
    uri: str,
    key: str | bytes | bytearray,
    http_method: _HTTPMethod,
    nonce: str | None = None,
    headers: dict[str, str] | None = None,
    body: str | None = None,
    ext: str = "",
    hash_algorithm: str = "hmac-sha-1",
    issue_time: datetime.datetime | None = None,
    draft: int = 0,
) -> dict[str, str]:
    """Add an `MAC Access Authentication`_ signature to headers.

    Unlike OAuth 1, this HMAC signature does not require inclusion of the
    request payload/body, neither does it use a combination of client_secret
    and token_secret but rather a mac_key provided together with the access
    token.

    Currently two algorithms are supported, "hmac-sha-1" and "hmac-sha-256",
    `extension algorithms`_ are not supported.

    Example MAC Authorization header, linebreaks added for clarity

    Authorization: MAC id="h480djs93hd8",
                       nonce="1336363200:dj83hs9s",
                       mac="bhCQXTVyfj5cmA9uKkPFx1zeOXM="

    .. _`MAC Access Authentication`: https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-01
    .. _`extension algorithms`: https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-01#section-7.1

    :param token:
    :param uri: Request URI.
    :param key: MAC given provided by token endpoint.
    :param http_method: HTTP Request method.
    :param nonce:
    :param headers: Request headers as a dictionary.
    :param body:
    :param ext:
    :param hash_algorithm: HMAC algorithm provided by token endpoint.
    :param issue_time: Time when the MAC credentials were issued (datetime).
    :param draft: MAC authentication specification version.
    :return: headers dictionary with the authorization field added.
    """

def prepare_bearer_uri(token: str, uri: str) -> str:
    """Add a `Bearer Token`_ to the request URI.
    Not recommended, use only if client can't use authorization header or body.

    http://www.example.com/path?access_token=h480djs93hd8

    .. _`Bearer Token`: https://tools.ietf.org/html/rfc6750

    :param token:
    :param uri:
    """

def prepare_bearer_headers(token: str, headers: dict[str, str] | None = None) -> dict[str, str]:
    """Add a `Bearer Token`_ to the request URI.
    Recommended method of passing bearer tokens.

    Authorization: Bearer h480djs93hd8

    .. _`Bearer Token`: https://tools.ietf.org/html/rfc6750

    :param token:
    :param headers:
    """

def prepare_bearer_body(token: str, body: str = "") -> str:
    """Add a `Bearer Token`_ to the request body.

    access_token=h480djs93hd8

    .. _`Bearer Token`: https://tools.ietf.org/html/rfc6750

    :param token:
    :param body:
    """

def random_token_generator(request: Request, refresh_token: bool = False) -> str:
    """
    :param request: OAuthlib request.
    :type request: oauthlib.common.Request
    :param refresh_token:
    """

def signed_token_generator(private_pem: str, **kwargs) -> Callable[[Request], str]:
    """
    :param private_pem:
    """

def get_token_from_header(request: Request) -> str | None:
    """
    Helper function to extract a token from the request header.

    :param request: OAuthlib request.
    :type request: oauthlib.common.Request
    :return: Return the token or None if the Authorization header is malformed.
    """

class TokenBase:
    def __call__(self, request: Request, refresh_token: bool = False) -> None: ...
    def validate_request(self, request: Request) -> bool:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def estimate_type(self, request: Request) -> int:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

class BearerToken(TokenBase):
    request_validator: RequestValidator | None
    token_generator: Callable[[Request], str]
    refresh_token_generator: Callable[[Request], str]
    expires_in: int | Callable[[Request], int]
    def __init__(
        self,
        request_validator: RequestValidator | None = None,
        token_generator: Callable[[Request], str] | None = None,
        expires_in: int | Callable[[Request], int] | None = None,
        refresh_token_generator: Callable[[Request], str] | None = None,
    ) -> None: ...
    def create_token(self, request: Request, refresh_token: bool = False, **kwargs) -> OAuth2Token:
        """
        Create a BearerToken, by default without refresh token.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param refresh_token:
        """

    def validate_request(self, request: Request) -> bool:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def estimate_type(self, request: Request) -> Literal[9, 5, 0]:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """
