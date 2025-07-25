from _typeshed import Incomplete
from logging import Logger
from typing import Any, Literal, Protocol, TypedDict, overload
from typing_extensions import TypeAlias

import requests
from oauthlib.oauth2 import Client
from requests.cookies import RequestsCookieJar

_Token: TypeAlias = dict[str, Incomplete]  # oauthlib.oauth2.Client.token

class _AccessTokenResponseHook(Protocol):
    def __call__(self, response: requests.Response, /) -> requests.Response: ...

class _RefreshTokenResponseHook(Protocol):
    def __call__(self, response: requests.Response, /) -> requests.Response: ...

class _ProtectedRequestHook(Protocol):
    def __call__(self, url, headers, data, /) -> tuple[Incomplete, Incomplete, Incomplete]: ...

class _ComplianceHooks(TypedDict):
    access_token_response: set[_AccessTokenResponseHook]
    refresh_token_response: set[_RefreshTokenResponseHook]
    protected_request: set[_ProtectedRequestHook]

log: Logger

class TokenUpdated(Warning):
    token: Incomplete
    def __init__(self, token) -> None: ...

class OAuth2Session(requests.Session):
    """Versatile OAuth 2 extension to :class:`requests.Session`.

    Supports any grant type adhering to :class:`oauthlib.oauth2.Client` spec
    including the four core OAuth 2 grants.

    Can be used to create authorization urls, fetch tokens and access protected
    resources using the :class:`requests.Session` interface you are used to.

    - :class:`oauthlib.oauth2.WebApplicationClient` (default): Authorization Code Grant
    - :class:`oauthlib.oauth2.MobileApplicationClient`: Implicit Grant
    - :class:`oauthlib.oauth2.LegacyApplicationClient`: Password Credentials Grant
    - :class:`oauthlib.oauth2.BackendApplicationClient`: Client Credentials Grant

    Note that the only time you will be using Implicit Grant from python is if
    you are driving a user agent able to obtain URL fragments.
    """

    redirect_uri: Incomplete
    state: Incomplete
    auto_refresh_url: str | None
    auto_refresh_kwargs: dict[str, Any]
    token_updater: Incomplete
    compliance_hook: _ComplianceHooks
    def __init__(
        self,
        client_id=None,
        client: Client | None = None,
        auto_refresh_url: str | None = None,
        auto_refresh_kwargs: dict[str, Any] | None = None,
        scope=None,
        redirect_uri=None,
        token=None,
        state=None,
        token_updater=None,
        pkce=None,
        **kwargs,
    ) -> None:
        """Construct a new OAuth 2 client session.

        :param client_id: Client id obtained during registration
        :param client: :class:`oauthlib.oauth2.Client` to be used. Default is
                       WebApplicationClient which is useful for any
                       hosted application but not mobile or desktop.
        :param scope: List of scopes you wish to request access to
        :param redirect_uri: Redirect URI you registered as callback
        :param token: Token dictionary, must include access_token
                      and token_type.
        :param state: State string used to prevent CSRF. This will be given
                      when creating the authorization url and must be supplied
                      when parsing the authorization response.
                      Can be either a string or a no argument callable.
        :auto_refresh_url: Refresh token endpoint URL, must be HTTPS. Supply
                           this if you wish the client to automatically refresh
                           your access tokens.
        :auto_refresh_kwargs: Extra arguments to pass to the refresh token
                              endpoint.
        :token_updater: Method with one argument, token, to be used to update
                        your token database on automatic token refresh. If not
                        set a TokenUpdated warning will be raised when a token
                        has been refreshed. This warning will carry the token
                        in its token argument.
        :param pkce: Set "S256" or "plain" to enable PKCE. Default is disabled.
        :param kwargs: Arguments to pass to the Session constructor.
        """

    @property
    def scope(self) -> Incomplete | None:  # oauthlib.oauth2.Client.scope
        """By default the scope from the client is used, except if overridden"""

    @scope.setter
    def scope(self, value: Incomplete | None) -> None: ...
    def new_state(self):
        """Generates a state string to be used in authorizations."""

    @property
    def client_id(self) -> Incomplete | None: ...  # oauthlib.oauth2.Client.client_id
    @client_id.setter
    def client_id(self, value: Incomplete | None) -> None: ...
    @client_id.deleter
    def client_id(self) -> None: ...
    @property
    def token(self): ...  # oauthlib.oauth2.Client.token
    @token.setter
    def token(self, value) -> None: ...
    @property
    def access_token(self): ...  # oauthlib.oauth2.Client.access_token
    @access_token.setter
    def access_token(self, value) -> None: ...
    @access_token.deleter
    def access_token(self) -> None: ...
    @property
    def authorized(self) -> bool:
        """Boolean that indicates whether this session has an OAuth token
        or not. If `self.authorized` is True, you can reasonably expect
        OAuth-protected requests to the resource to succeed. If
        `self.authorized` is False, you need the user to go through the OAuth
        authentication dance before OAuth-protected requests to the resource
        will succeed.
        """

    def authorization_url(self, url: str, state=None, **kwargs) -> tuple[str, str]:
        """Form an authorization URL.

        :param url: Authorization endpoint url, must be HTTPS.
        :param state: An optional state string for CSRF protection. If not
                      given it will be generated for you.
        :param kwargs: Extra parameters to include.
        :return: authorization_url, state
        """

    def fetch_token(
        self,
        token_url: str,
        code=None,
        authorization_response=None,
        body: str = "",
        auth=None,
        username=None,
        password=None,
        method: str = "POST",
        force_querystring: bool = False,
        timeout=None,
        headers=None,
        verify: bool | None = None,
        proxies=None,
        include_client_id=None,
        client_secret=None,
        cert=None,
        **kwargs,
    ) -> _Token:
        """Generic method for fetching an access token from the token endpoint.

        If you are using the MobileApplicationClient you will want to use
        `token_from_fragment` instead of `fetch_token`.

        The current implementation enforces the RFC guidelines.

        :param token_url: Token endpoint URL, must use HTTPS.
        :param code: Authorization code (used by WebApplicationClients).
        :param authorization_response: Authorization response URL, the callback
                                       URL of the request back to you. Used by
                                       WebApplicationClients instead of code.
        :param body: Optional application/x-www-form-urlencoded body to add the
                     include in the token request. Prefer kwargs over body.
        :param auth: An auth tuple or method as accepted by `requests`.
        :param username: Username required by LegacyApplicationClients to appear
                         in the request body.
        :param password: Password required by LegacyApplicationClients to appear
                         in the request body.
        :param method: The HTTP method used to make the request. Defaults
                       to POST, but may also be GET. Other methods should
                       be added as needed.
        :param force_querystring: If True, force the request body to be sent
            in the querystring instead.
        :param timeout: Timeout of the request in seconds.
        :param headers: Dict to default request headers with.
        :param verify: Verify SSL certificate.
        :param proxies: The `proxies` argument is passed onto `requests`.
        :param include_client_id: Should the request body include the
                                  `client_id` parameter. Default is `None`,
                                  which will attempt to autodetect. This can be
                                  forced to always include (True) or never
                                  include (False).
        :param client_secret: The `client_secret` paired to the `client_id`.
                              This is generally required unless provided in the
                              `auth` tuple. If the value is `None`, it will be
                              omitted from the request, however if the value is
                              an empty string, an empty string will be sent.
        :param cert: Client certificate to send for OAuth 2.0 Mutual-TLS Client
                     Authentication (draft-ietf-oauth-mtls). Can either be the
                     path of a file containing the private key and certificate or
                     a tuple of two filenames for certificate and key.
        :param kwargs: Extra parameters to include in the token request.
        :return: A token dict
        """

    def token_from_fragment(self, authorization_response: str) -> _Token:
        """Parse token from the URI fragment, used by MobileApplicationClients.

        :param authorization_response: The full URL of the redirect back to you
        :return: A token dict
        """

    def refresh_token(
        self,
        token_url: str,
        refresh_token=None,
        body: str = "",
        auth=None,
        timeout=None,
        headers=None,
        verify: bool | None = None,
        proxies=None,
        **kwargs,
    ) -> _Token:
        """Fetch a new access token using a refresh token.

        :param token_url: The token endpoint, must be HTTPS.
        :param refresh_token: The refresh_token to use.
        :param body: Optional application/x-www-form-urlencoded body to add the
                     include in the token request. Prefer kwargs over body.
        :param auth: An auth tuple or method as accepted by `requests`.
        :param timeout: Timeout of the request in seconds.
        :param headers: A dict of headers to be used by `requests`.
        :param verify: Verify SSL certificate.
        :param proxies: The `proxies` argument will be passed to `requests`.
        :param kwargs: Extra parameters to include in the token request.
        :return: A token dict
        """

    def request(  # type: ignore[override]
        self,
        method: str | bytes,
        url: str | bytes,
        data: requests.sessions._Data | None = None,
        headers: requests.sessions._HeadersUpdateMapping | None = None,
        withhold_token: bool = False,
        client_id=None,
        client_secret=None,
        files: requests.sessions._Files | None = None,
        *,
        params: requests.sessions._Params | None = None,
        cookies: None | RequestsCookieJar | requests.sessions._TextMapping = None,
        auth: requests.sessions._Auth | None = None,
        timeout: requests.sessions._Timeout | None = None,
        allow_redirects: bool = True,
        proxies: requests.sessions._TextMapping | None = None,
        hooks: requests.sessions._HooksInput | None = None,
        stream: bool | None = None,
        verify: requests.sessions._Verify | None = None,
        cert: requests.sessions._Cert | None = None,
        json=None,
    ) -> requests.Response:
        """Intercept all requests and add the OAuth 2 token if present."""

    @overload
    def register_compliance_hook(self, hook_type: Literal["access_token_response"], hook: _AccessTokenResponseHook) -> None:
        """Register a hook for request/response tweaking.

        Available hooks are:
            access_token_response invoked before token parsing.
            refresh_token_response invoked before refresh token parsing.
            protected_request invoked before making a request.
            access_token_request invoked before making a token fetch request.
            refresh_token_request invoked before making a refresh request.

        If you find a new hook is needed please send a GitHub PR request
        or open an issue.
        """

    @overload
    def register_compliance_hook(self, hook_type: Literal["refresh_token_response"], hook: _RefreshTokenResponseHook) -> None: ...
    @overload
    def register_compliance_hook(self, hook_type: Literal["protected_request"], hook: _ProtectedRequestHook) -> None: ...
