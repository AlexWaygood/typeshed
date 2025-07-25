"""
oauthlib.oauth2.rfc6749
~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for consuming OAuth 2.0 RFC6749.
"""

from _typeshed import ConvertibleToInt, Incomplete
from collections.abc import Callable
from typing import Final, Literal
from typing_extensions import TypeAlias

from oauthlib.common import _HTTPMethod
from oauthlib.oauth2.rfc6749.tokens import OAuth2Token

_TokenPlacement: TypeAlias = Literal["auth_header", "query", "body"]

AUTH_HEADER: Final[_TokenPlacement]
URI_QUERY: Final[_TokenPlacement]
BODY: Final[_TokenPlacement]
FORM_ENC_HEADERS: Final[dict[str, str]]

class Client:
    """Base OAuth2 client responsible for access token management.

    This class also acts as a generic interface providing methods common to all
    client types such as ``prepare_authorization_request`` and
    ``prepare_token_revocation_request``. The ``prepare_x_request`` methods are
    the recommended way of interacting with clients (as opposed to the abstract
    prepare uri/body/etc methods). They are recommended over the older set
    because they are easier to use (more consistent) and add a few additional
    security checks, such as HTTPS and state checking.

    Some of these methods require further implementation only provided by the
    specific purpose clients such as
    :py:class:`oauthlib.oauth2.MobileApplicationClient` and thus you should always
    seek to use the client class matching the OAuth workflow you need. For
    Python, this is usually :py:class:`oauthlib.oauth2.WebApplicationClient`.

    """

    refresh_token_key: str
    client_id: str
    default_token_placement: _TokenPlacement
    token_type: str
    access_token: str | None
    refresh_token: str | None
    mac_key: str | bytes | bytearray | None
    mac_algorithm: str | None
    token: dict[str, Incomplete]
    scope: str | set[object] | tuple[object] | list[object]
    state_generator: Callable[[], str]
    state: str | None
    redirect_url: str | None
    code: str | None
    expires_in: ConvertibleToInt | None
    code_verifier: str | None
    code_challenge: str | None
    code_challenge_method: str | None
    def __init__(
        self,
        client_id: str,
        default_token_placement: _TokenPlacement = "auth_header",
        token_type: str = "Bearer",
        access_token: str | None = None,
        refresh_token: str | None = None,
        mac_key: str | bytes | bytearray | None = None,
        mac_algorithm: str | None = None,
        token: dict[str, Incomplete] | None = None,
        scope: str | set[object] | tuple[object] | list[object] | None = None,
        state: str | None = None,
        redirect_url: str | None = None,
        state_generator: Callable[[], str] = ...,
        code_verifier: str | None = None,
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
        **kwargs,
    ) -> None:
        """Initialize a client with commonly used attributes.

        :param client_id: Client identifier given by the OAuth provider upon
        registration.

        :param default_token_placement: Tokens can be supplied in the Authorization
        header (default), the URL query component (``query``) or the request
        body (``body``).

        :param token_type: OAuth 2 token type. Defaults to Bearer. Change this
        if you specify the ``access_token`` parameter and know it is of a
        different token type, such as a MAC, JWT or SAML token. Can
        also be supplied as ``token_type`` inside the ``token`` dict parameter.

        :param access_token: An access token (string) used to authenticate
        requests to protected resources. Can also be supplied inside the
        ``token`` dict parameter.

        :param refresh_token: A refresh token (string) used to refresh expired
        tokens. Can also be supplied inside the ``token`` dict parameter.

        :param mac_key: Encryption key used with MAC tokens.

        :param mac_algorithm:  Hashing algorithm for MAC tokens.

        :param token: A dict of token attributes such as ``access_token``,
        ``token_type`` and ``expires_at``.

        :param scope: A list of default scopes to request authorization for.

        :param state: A CSRF protection string used during authorization.

        :param redirect_url: The redirection endpoint on the client side to which
        the user returns after authorization.

        :param state_generator: A no argument state generation callable. Defaults
        to :py:meth:`oauthlib.common.generate_token`.

        :param code_verifier: PKCE parameter. A cryptographically random string that is used to correlate the
        authorization request to the token request.

        :param code_challenge: PKCE parameter. A challenge derived from the code verifier that is sent in the
        authorization request, to be verified against later.

        :param code_challenge_method: PKCE parameter. A method that was used to derive code challenge.
        Defaults to "plain" if not present in the request.
        """

    @property
    def token_types(
        self,
    ) -> dict[
        Literal["Bearer", "MAC"],
        Callable[
            [str, str, str | None, dict[str, str] | None, str | None, Incomplete], tuple[str, dict[str, str] | None, str | None]
        ],
    ]:
        """Supported token types and their respective methods

        Additional tokens can be supported by extending this dictionary.

        The Bearer token spec is stable and safe to use.

        The MAC token spec is not yet stable and support for MAC tokens
        is experimental and currently matching version 00 of the spec.
        """

    def prepare_request_uri(self, *args, **kwargs) -> str:
        """Abstract method used to create request URIs."""

    def prepare_request_body(self, *args, **kwargs) -> str:
        """Abstract method used to create request bodies."""

    def parse_request_uri_response(self, *args, **kwargs) -> dict[str, str]:
        """Abstract method used to parse redirection responses."""

    def add_token(
        self,
        uri: str,
        http_method: _HTTPMethod = "GET",
        body: str | None = None,
        headers: dict[str, str] | None = None,
        token_placement: _TokenPlacement | None = None,
        **kwargs,
    ) -> tuple[str, dict[str, str] | None, str | None]:
        """Add token to the request uri, body or authorization header.

        The access token type provides the client with the information
        required to successfully utilize the access token to make a protected
        resource request (along with type-specific attributes).  The client
        MUST NOT use an access token if it does not understand the token
        type.

        For example, the "bearer" token type defined in
        [`I-D.ietf-oauth-v2-bearer`_] is utilized by simply including the access
        token string in the request:

        .. code-block:: http

            GET /resource/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer mF_9.B5f-4.1JqM

        while the "mac" token type defined in [`I-D.ietf-oauth-v2-http-mac`_] is
        utilized by issuing a MAC key together with the access token which is
        used to sign certain components of the HTTP requests:

        .. code-block:: http

            GET /resource/1 HTTP/1.1
            Host: example.com
            Authorization: MAC id="h480djs93hd8",
                                nonce="274312:dj83hs9s",
                                mac="kDZvddkndxvhGRXZhvuDjEWhGeE="

        .. _`I-D.ietf-oauth-v2-bearer`: https://tools.ietf.org/html/rfc6749#section-12.2
        .. _`I-D.ietf-oauth-v2-http-mac`: https://tools.ietf.org/html/rfc6749#section-12.2
        """

    def prepare_authorization_request(
        self,
        authorization_url: str,
        state: str | None = None,
        redirect_url: str | None = None,
        scope: str | set[object] | tuple[object] | list[object] | None = None,
        **kwargs,
    ) -> tuple[str, dict[str, str], str]:
        """Prepare the authorization request.

        This is the first step in many OAuth flows in which the user is
        redirected to a certain authorization URL. This method adds
        required parameters to the authorization URL.

        :param authorization_url: Provider authorization endpoint URL.
        :param state: CSRF protection string. Will be automatically created if
            not provided. The generated state is available via the ``state``
            attribute. Clients should verify that the state is unchanged and
            present in the authorization response. This verification is done
            automatically if using the ``authorization_response`` parameter
            with ``prepare_token_request``.
        :param redirect_url: Redirect URL to which the user will be returned
            after authorization. Must be provided unless previously setup with
            the provider. If provided then it must also be provided in the
            token request.
        :param scope: List of scopes to request. Must be equal to
            or a subset of the scopes granted when obtaining the refresh
            token. If none is provided, the ones provided in the constructor are
            used.
        :param kwargs: Additional parameters to included in the request.
        :returns: The prepared request tuple with (url, headers, body).
        """

    def prepare_token_request(
        self,
        token_url: str,
        authorization_response: str | None = None,
        redirect_url: str | None = None,
        state: str | None = None,
        body: str = "",
        **kwargs,
    ) -> tuple[str, dict[str, str], str]:
        """Prepare a token creation request.

        Note that these requests usually require client authentication, either
        by including client_id or a set of provider specific authentication
        credentials.

        :param token_url: Provider token creation endpoint URL.
        :param authorization_response: The full redirection URL string, i.e.
            the location to which the user was redirected after successful
            authorization. Used to mine credentials needed to obtain a token
            in this step, such as authorization code.
        :param redirect_url: The redirect_url supplied with the authorization
            request (if there was one).
        :param state:
        :param body: Existing request body (URL encoded string) to embed parameters
                     into. This may contain extra parameters. Default ''.
        :param kwargs: Additional parameters to included in the request.
        :returns: The prepared request tuple with (url, headers, body).
        """

    def prepare_refresh_token_request(
        self,
        token_url: str,
        refresh_token: str | None = None,
        body: str = "",
        scope: str | set[object] | tuple[object] | list[object] | None = None,
        **kwargs,
    ) -> tuple[str, dict[str, str], str]:
        """Prepare an access token refresh request.

        Expired access tokens can be replaced by new access tokens without
        going through the OAuth dance if the client obtained a refresh token.
        This refresh token and authentication credentials can be used to
        obtain a new access token, and possibly a new refresh token.

        :param token_url: Provider token refresh endpoint URL.
        :param refresh_token: Refresh token string.
        :param body: Existing request body (URL encoded string) to embed parameters
            into. This may contain extra parameters. Default ''.
        :param scope: List of scopes to request. Must be equal to
            or a subset of the scopes granted when obtaining the refresh
            token. If none is provided, the ones provided in the constructor are
            used.
        :param kwargs: Additional parameters to included in the request.
        :returns: The prepared request tuple with (url, headers, body).
        """

    def prepare_token_revocation_request(
        self,
        revocation_url: str,
        token: str,
        token_type_hint: Literal["access_token", "refresh_token"] | None = "access_token",
        body: str = "",
        callback: Callable[[Incomplete], Incomplete] | None = None,
        **kwargs,
    ):
        """Prepare a token revocation request.

        :param revocation_url: Provider token revocation endpoint URL.
        :param token: The access or refresh token to be revoked (string).
        :param token_type_hint: ``"access_token"`` (default) or
            ``"refresh_token"``. This is optional and if you wish to not pass it you
            must provide ``token_type_hint=None``.
        :param body:
        :param callback: A jsonp callback such as ``package.callback`` to be invoked
            upon receiving the response. Not that it should not include a () suffix.
        :param kwargs: Additional parameters to included in the request.
        :returns: The prepared request tuple with (url, headers, body).

        Note that JSONP request may use GET requests as the parameters will
        be added to the request URL query as opposed to the request body.

        An example of a revocation request

        .. code-block:: http

            POST /revoke HTTP/1.1
            Host: server.example.com
            Content-Type: application/x-www-form-urlencoded
            Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW

            token=45ghiukldjahdnhzdauz&token_type_hint=refresh_token

        An example of a jsonp revocation request

        .. code-block:: http

            GET /revoke?token=agabcdefddddafdd&callback=package.myCallback HTTP/1.1
            Host: server.example.com
            Content-Type: application/x-www-form-urlencoded
            Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW

        and an error response

        .. code-block:: javascript

            package.myCallback({"error":"unsupported_token_type"});

        Note that these requests usually require client credentials, client_id in
        the case for public clients and provider specific authentication
        credentials for confidential clients.
        """

    def parse_request_body_response(
        self, body: str, scope: str | set[object] | tuple[object] | list[object] | None = None, **kwargs
    ) -> OAuth2Token:
        """Parse the JSON response body.

        If the access token request is valid and authorized, the
        authorization server issues an access token as described in
        `Section 5.1`_.  A refresh token SHOULD NOT be included.  If the request
        failed client authentication or is invalid, the authorization server
        returns an error response as described in `Section 5.2`_.

        :param body: The response body from the token request.
        :param scope: Scopes originally requested. If none is provided, the ones
            provided in the constructor are used.
        :return: Dictionary of token parameters.
        :raises: Warning if scope has changed. :py:class:`oauthlib.oauth2.errors.OAuth2Error`
            if response is invalid.

        These response are json encoded and could easily be parsed without
        the assistance of OAuthLib. However, there are a few subtle issues
        to be aware of regarding the response which are helpfully addressed
        through the raising of various errors.

        A successful response should always contain

        **access_token**
                The access token issued by the authorization server. Often
                a random string.

        **token_type**
            The type of the token issued as described in `Section 7.1`_.
            Commonly ``Bearer``.

        While it is not mandated it is recommended that the provider include

        **expires_in**
            The lifetime in seconds of the access token.  For
            example, the value "3600" denotes that the access token will
            expire in one hour from the time the response was generated.
            If omitted, the authorization server SHOULD provide the
            expiration time via other means or document the default value.

         **scope**
            Providers may supply this in all responses but are required to only
            if it has changed since the authorization request.

        .. _`Section 5.1`: https://tools.ietf.org/html/rfc6749#section-5.1
        .. _`Section 5.2`: https://tools.ietf.org/html/rfc6749#section-5.2
        .. _`Section 7.1`: https://tools.ietf.org/html/rfc6749#section-7.1
        """

    def prepare_refresh_body(
        self,
        body: str = "",
        refresh_token: str | None = None,
        scope: str | set[object] | tuple[object] | list[object] | None = None,
        **kwargs,
    ) -> str:
        """Prepare an access token request, using a refresh token.

        If the authorization server issued a refresh token to the client, the
        client makes a refresh request to the token endpoint by adding the
        following parameters using the `application/x-www-form-urlencoded`
        format in the HTTP request entity-body:

        :param refresh_token: REQUIRED.  The refresh token issued to the client.
        :param scope:  OPTIONAL.  The scope of the access request as described by
            Section 3.3.  The requested scope MUST NOT include any scope
            not originally granted by the resource owner, and if omitted is
            treated as equal to the scope originally granted by the
            resource owner. Note that if none is provided, the ones provided
            in the constructor are used if any.
        """

    def create_code_verifier(self, length: int) -> str:
        """Create PKCE **code_verifier** used in computing **code_challenge**.
        See `RFC7636 Section 4.1`_

        :param length: REQUIRED. The length of the code_verifier.

        The client first creates a code verifier, "code_verifier", for each
        OAuth 2.0 [RFC6749] Authorization Request, in the following manner:

        .. code-block:: text

               code_verifier = high-entropy cryptographic random STRING using the
               unreserved characters [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
               from Section 2.3 of [RFC3986], with a minimum length of 43 characters
               and a maximum length of 128 characters.

        .. _`RFC7636 Section 4.1`: https://tools.ietf.org/html/rfc7636#section-4.1
        """

    def create_code_challenge(self, code_verifier: str, code_challenge_method: str | None = None) -> str:
        """Create PKCE **code_challenge** derived from the  **code_verifier**.
        See `RFC7636 Section 4.2`_

        :param code_verifier: REQUIRED. The **code_verifier** generated from `create_code_verifier()`.
        :param code_challenge_method: OPTIONAL. The method used to derive the **code_challenge**. Acceptable values include `S256`. DEFAULT is `plain`.

               The client then creates a code challenge derived from the code
               verifier by using one of the following transformations on the code
               verifier::

                   plain
                      code_challenge = code_verifier
                   S256
                      code_challenge = BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))

               If the client is capable of using `S256`, it MUST use `S256`, as
               `S256` is Mandatory To Implement (MTI) on the server.  Clients are
               permitted to use `plain` only if they cannot support `S256` for some
               technical reason and know via out-of-band configuration that the
               server supports `plain`.

               The plain transformation is for compatibility with existing
               deployments and for constrained environments that can't use the S256 transformation.

        .. _`RFC7636 Section 4.2`: https://tools.ietf.org/html/rfc7636#section-4.2
        """

    def populate_code_attributes(self, response: dict[str, Incomplete]) -> None:
        """Add attributes from an auth code response to self."""

    def populate_token_attributes(self, response: dict[str, Incomplete]) -> None:
        """Add attributes from a token exchange response to self."""
