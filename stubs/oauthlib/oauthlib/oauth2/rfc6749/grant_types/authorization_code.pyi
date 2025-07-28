"""
oauthlib.oauth2.rfc6749.grant_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from _typeshed import Incomplete
from logging import Logger

from oauthlib.common import Request

from ..tokens import TokenBase
from .base import GrantTypeBase

log: Logger

def code_challenge_method_s256(verifier: str, challenge: str) -> bool:
    """
    If the "code_challenge_method" from `Section 4.3`_ was "S256", the
    received "code_verifier" is hashed by SHA-256, base64url-encoded, and
    then compared to the "code_challenge", i.e.:

    BASE64URL-ENCODE(SHA256(ASCII(code_verifier))) == code_challenge

    How to implement a base64url-encoding
    function without padding, based upon the standard base64-encoding
    function that uses padding.

    To be concrete, example C# code implementing these functions is shown
    below.  Similar code could be used in other languages.

    static string base64urlencode(byte [] arg)
    {
        string s = Convert.ToBase64String(arg); // Regular base64 encoder
        s = s.Split('=')[0]; // Remove any trailing '='s
        s = s.Replace('+', '-'); // 62nd char of encoding
        s = s.Replace('/', '_'); // 63rd char of encoding
        return s;
    }

    In python urlsafe_b64encode is already replacing '+' and '/', but preserve
    the trailing '='. So we have to remove it.

    .. _`Section 4.3`: https://tools.ietf.org/html/rfc7636#section-4.3
    """

def code_challenge_method_plain(verifier: str, challenge: str) -> bool:
    """
    If the "code_challenge_method" from `Section 4.3`_ was "plain", they are
    compared directly, i.e.:

    code_verifier == code_challenge.

    .. _`Section 4.3`: https://tools.ietf.org/html/rfc7636#section-4.3
    """

class AuthorizationCodeGrant(GrantTypeBase):
    """`Authorization Code Grant`_

    The authorization code grant type is used to obtain both access
    tokens and refresh tokens and is optimized for confidential clients.
    Since this is a redirection-based flow, the client must be capable of
    interacting with the resource owner's user-agent (typically a web
    browser) and capable of receiving incoming requests (via redirection)
    from the authorization server::

        +----------+
        | Resource |
        |   Owner  |
        |          |
        +----------+
             ^
             |
            (B)
        +----|-----+          Client Identifier      +---------------+
        |         -+----(A)-- & Redirection URI ---->|               |
        |  User-   |                                 | Authorization |
        |  Agent  -+----(B)-- User authenticates --->|     Server    |
        |          |                                 |               |
        |         -+----(C)-- Authorization Code ---<|               |
        +-|----|---+                                 +---------------+
          |    |                                         ^      v
         (A)  (C)                                        |      |
          |    |                                         |      |
          ^    v                                         |      |
        +---------+                                      |      |
        |         |>---(D)-- Authorization Code ---------'      |
        |  Client |          & Redirection URI                  |
        |         |                                             |
        |         |<---(E)----- Access Token -------------------'
        +---------+       (w/ Optional Refresh Token)

    Note: The lines illustrating steps (A), (B), and (C) are broken into
    two parts as they pass through the user-agent.

    Figure 3: Authorization Code Flow

    The flow illustrated in Figure 3 includes the following steps:

    (A)  The client initiates the flow by directing the resource owner's
         user-agent to the authorization endpoint.  The client includes
         its client identifier, requested scope, local state, and a
         redirection URI to which the authorization server will send the
         user-agent back once access is granted (or denied).

    (B)  The authorization server authenticates the resource owner (via
         the user-agent) and establishes whether the resource owner
         grants or denies the client's access request.

    (C)  Assuming the resource owner grants access, the authorization
         server redirects the user-agent back to the client using the
         redirection URI provided earlier (in the request or during
         client registration).  The redirection URI includes an
         authorization code and any local state provided by the client
         earlier.

    (D)  The client requests an access token from the authorization
         server's token endpoint by including the authorization code
         received in the previous step.  When making the request, the
         client authenticates with the authorization server.  The client
         includes the redirection URI used to obtain the authorization
         code for verification.

    (E)  The authorization server authenticates the client, validates the
         authorization code, and ensures that the redirection URI
         received matches the URI used to redirect the client in
         step (C).  If valid, the authorization server responds back with
         an access token and, optionally, a refresh token.

    OAuth 2.0 public clients utilizing the Authorization Code Grant are
    susceptible to the authorization code interception attack.

    A technique to mitigate against the threat through the use of Proof Key for Code
    Exchange (PKCE, pronounced "pixy") is implemented in the current oauthlib
    implementation.

    .. _`Authorization Code Grant`: https://tools.ietf.org/html/rfc6749#section-4.1
    .. _`PKCE`: https://tools.ietf.org/html/rfc7636
    """

    default_response_mode: str
    response_types: list[str]
    def create_authorization_code(self, request: Request) -> dict[str, str]:
        """
        Generates an authorization grant represented as a dictionary.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def create_authorization_response(
        self, request: Request, token_handler: TokenBase
    ) -> tuple[dict[str, str], None, int | None]:
        """
        The client constructs the request URI by adding the following
        parameters to the query component of the authorization endpoint URI
        using the "application/x-www-form-urlencoded" format, per `Appendix B`_:

        response_type
                REQUIRED.  Value MUST be set to "code" for standard OAuth2
                authorization flow.  For OpenID Connect it must be one of
                "code token", "code id_token", or "code token id_token" - we
                essentially test that "code" appears in the response_type.
        client_id
                REQUIRED.  The client identifier as described in `Section 2.2`_.
        redirect_uri
                OPTIONAL.  As described in `Section 3.1.2`_.
        scope
                OPTIONAL.  The scope of the access request as described by
                `Section 3.3`_.
        state
                RECOMMENDED.  An opaque value used by the client to maintain
                state between the request and callback.  The authorization
                server includes this value when redirecting the user-agent back
                to the client.  The parameter SHOULD be used for preventing
                cross-site request forgery as described in `Section 10.12`_.

        The client directs the resource owner to the constructed URI using an
        HTTP redirection response, or by other means available to it via the
        user-agent.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param token_handler: A token handler instance, for example of type
                              oauthlib.oauth2.BearerToken.
        :returns: headers, body, status
        :raises: FatalClientError on invalid redirect URI or client id.

        A few examples::

            >>> from your_validator import your_validator
            >>> request = Request('https://example.com/authorize?client_id=valid'
            ...                   '&redirect_uri=http%3A%2F%2Fclient.com%2F')
            >>> from oauthlib.common import Request
            >>> from oauthlib.oauth2 import AuthorizationCodeGrant, BearerToken
            >>> token = BearerToken(your_validator)
            >>> grant = AuthorizationCodeGrant(your_validator)
            >>> request.scopes = ['authorized', 'in', 'some', 'form']
            >>> grant.create_authorization_response(request, token)
            (u'http://client.com/?error=invalid_request&error_description=Missing+response_type+parameter.', None, None, 400)
            >>> request = Request('https://example.com/authorize?client_id=valid'
            ...                   '&redirect_uri=http%3A%2F%2Fclient.com%2F'
            ...                   '&response_type=code')
            >>> request.scopes = ['authorized', 'in', 'some', 'form']
            >>> grant.create_authorization_response(request, token)
            (u'http://client.com/?code=u3F05aEObJuP2k7DordviIgW5wl52N', None, None, 200)
            >>> # If the client id or redirect uri fails validation
            >>> grant.create_authorization_response(request, token)
            Traceback (most recent call last):
                File "<stdin>", line 1, in <module>
                File "oauthlib/oauth2/rfc6749/grant_types.py", line 515, in create_authorization_response
                    >>> grant.create_authorization_response(request, token)
                File "oauthlib/oauth2/rfc6749/grant_types.py", line 591, in validate_authorization_request
            oauthlib.oauth2.rfc6749.errors.InvalidClientIdError

        .. _`Appendix B`: https://tools.ietf.org/html/rfc6749#appendix-B
        .. _`Section 2.2`: https://tools.ietf.org/html/rfc6749#section-2.2
        .. _`Section 3.1.2`: https://tools.ietf.org/html/rfc6749#section-3.1.2
        .. _`Section 3.3`: https://tools.ietf.org/html/rfc6749#section-3.3
        .. _`Section 10.12`: https://tools.ietf.org/html/rfc6749#section-10.12
        """

    def create_token_response(self, request: Request, token_handler: TokenBase) -> tuple[dict[str, str], str, int | None]:
        """Validate the authorization code.

        The client MUST NOT use the authorization code more than once. If an
        authorization code is used more than once, the authorization server
        MUST deny the request and SHOULD revoke (when possible) all tokens
        previously issued based on that authorization code. The authorization
        code is bound to the client identifier and redirection URI.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param token_handler: A token handler instance, for example of type
                              oauthlib.oauth2.BearerToken.

        """

    def validate_authorization_request(self, request: Request) -> tuple[Incomplete, dict[str, Incomplete]]:
        """Check the authorization request for normal and fatal errors.

        A normal error could be a missing response_type parameter or the client
        attempting to access scope it is not allowed to ask authorization for.
        Normal errors can safely be included in the redirection URI and
        sent back to the client.

        Fatal errors occur when the client_id or redirect_uri is invalid or
        missing. These must be caught by the provider and handled, how this
        is done is outside of the scope of OAuthLib but showing an error
        page describing the issue is a good idea.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def validate_token_request(self, request: Request) -> None:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def validate_code_challenge(self, challenge: str, challenge_method: str, verifier: str) -> bool: ...
