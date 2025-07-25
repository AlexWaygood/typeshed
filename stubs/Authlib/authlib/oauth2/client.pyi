from _typeshed import Incomplete

from authlib.oauth2 import ClientAuth, OAuth2Error, TokenAuth

DEFAULT_HEADERS: Incomplete

class OAuth2Client:
    """Construct a new OAuth 2 protocol client.

    :param session: Requests session object to communicate with
                    authorization server.
    :param client_id: Client ID, which you get from client registration.
    :param client_secret: Client Secret, which you get from registration.
    :param token_endpoint_auth_method: client authentication method for
        token endpoint.
    :param revocation_endpoint_auth_method: client authentication method for
        revocation endpoint.
    :param scope: Scope that you needed to access user resources.
    :param state: Shared secret to prevent CSRF attack.
    :param redirect_uri: Redirect URI you registered as callback.
    :param code_challenge_method: PKCE method name, only S256 is supported.
    :param token: A dict of token attributes such as ``access_token``,
        ``token_type`` and ``expires_at``.
    :param token_placement: The place to put token in HTTP request. Available
        values: "header", "body", "uri".
    :param update_token: A function for you to update token. It accept a
        :class:`OAuth2Token` as parameter.
    :param leeway: Time window in seconds before the actual expiration of the
        authentication token, that the token is considered expired and will
        be refreshed.
    """

    client_auth_class = ClientAuth
    token_auth_class = TokenAuth
    oauth_error_class = OAuth2Error
    EXTRA_AUTHORIZE_PARAMS: Incomplete
    SESSION_REQUEST_PARAMS: Incomplete
    session: Incomplete
    client_id: Incomplete
    client_secret: Incomplete
    state: Incomplete
    token_endpoint_auth_method: Incomplete
    revocation_endpoint_auth_method: Incomplete
    scope: Incomplete
    redirect_uri: Incomplete
    code_challenge_method: Incomplete
    token_auth: Incomplete
    update_token: Incomplete
    metadata: Incomplete
    compliance_hook: Incomplete
    leeway: Incomplete
    def __init__(
        self,
        session,
        client_id=None,
        client_secret=None,
        token_endpoint_auth_method=None,
        revocation_endpoint_auth_method=None,
        scope=None,
        state=None,
        redirect_uri=None,
        code_challenge_method=None,
        token=None,
        token_placement: str = "header",
        update_token=None,
        leeway: int = 60,
        **metadata,
    ) -> None: ...
    def register_client_auth_method(self, auth) -> None:
        """Extend client authenticate for token endpoint.

        :param auth: an instance to sign the request
        """

    def client_auth(self, auth_method): ...
    @property
    def token(self): ...
    @token.setter
    def token(self, token) -> None: ...
    def create_authorization_url(self, url, state=None, code_verifier=None, **kwargs):
        """Generate an authorization URL and state.

        :param url: Authorization endpoint url, must be HTTPS.
        :param state: An optional state string for CSRF protection. If not
                      given it will be generated for you.
        :param code_verifier: An optional code_verifier for code challenge.
        :param kwargs: Extra parameters to include.
        :return: authorization_url, state
        """

    def fetch_token(
        self, url=None, body: str = "", method: str = "POST", headers=None, auth=None, grant_type=None, state=None, **kwargs
    ):
        """Generic method for fetching an access token from the token endpoint.

        :param url: Access Token endpoint URL, if not configured,
                    ``authorization_response`` is used to extract token from
                    its fragment (implicit way).
        :param body: Optional application/x-www-form-urlencoded body to add the
                     include in the token request. Prefer kwargs over body.
        :param method: The HTTP method used to make the request. Defaults
                       to POST, but may also be GET. Other methods should
                       be added as needed.
        :param headers: Dict to default request headers with.
        :param auth: An auth tuple or method as accepted by requests.
        :param grant_type: Use specified grant_type to fetch token
        :return: A :class:`OAuth2Token` object (a dict too).
        """

    def token_from_fragment(self, authorization_response, state=None): ...
    def refresh_token(self, url=None, refresh_token=None, body: str = "", auth=None, headers=None, **kwargs):
        """Fetch a new access token using a refresh token.

        :param url: Refresh Token endpoint, must be HTTPS.
        :param refresh_token: The refresh_token to use.
        :param body: Optional application/x-www-form-urlencoded body to add the
                     include in the token request. Prefer kwargs over body.
        :param auth: An auth tuple or method as accepted by requests.
        :param headers: Dict to default request headers with.
        :return: A :class:`OAuth2Token` object (a dict too).
        """

    def ensure_active_token(self, token=None): ...
    def revoke_token(self, url, token=None, token_type_hint=None, body=None, auth=None, headers=None, **kwargs):
        """Revoke token method defined via `RFC7009`_.

        :param url: Revoke Token endpoint, must be HTTPS.
        :param token: The token to be revoked.
        :param token_type_hint: The type of the token that to be revoked.
                                It can be "access_token" or "refresh_token".
        :param body: Optional application/x-www-form-urlencoded body to add the
                     include in the token request. Prefer kwargs over body.
        :param auth: An auth tuple or method as accepted by requests.
        :param headers: Dict to default request headers with.
        :return: Revocation Response

        .. _`RFC7009`: https://tools.ietf.org/html/rfc7009
        """

    def introspect_token(self, url, token=None, token_type_hint=None, body=None, auth=None, headers=None, **kwargs):
        """Implementation of OAuth 2.0 Token Introspection defined via `RFC7662`_.

        :param url: Introspection Endpoint, must be HTTPS.
        :param token: The token to be introspected.
        :param token_type_hint: The type of the token that to be revoked.
                                It can be "access_token" or "refresh_token".
        :param body: Optional application/x-www-form-urlencoded body to add the
                     include in the token request. Prefer kwargs over body.
        :param auth: An auth tuple or method as accepted by requests.
        :param headers: Dict to default request headers with.
        :return: Introspection Response

        .. _`RFC7662`: https://tools.ietf.org/html/rfc7662
        """

    def register_compliance_hook(self, hook_type, hook) -> None:
        """Register a hook for request/response tweaking.

        Available hooks are:

        * access_token_response: invoked before token parsing.
        * refresh_token_request: invoked before refreshing token.
        * refresh_token_response: invoked before refresh token parsing.
        * protected_request: invoked before making a request.
        * revoke_token_request: invoked before revoking a token.
        * introspect_token_request: invoked before introspecting a token.
        """

    def parse_response_token(self, resp): ...
    def __del__(self) -> None: ...
