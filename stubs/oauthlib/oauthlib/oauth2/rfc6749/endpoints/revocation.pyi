"""
oauthlib.oauth2.rfc6749.endpoint.revocation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An implementation of the OAuth 2 `Token Revocation`_ spec (draft 11).

.. _`Token Revocation`: https://tools.ietf.org/html/draft-ietf-oauth-revocation-11
"""

from logging import Logger
from typing import Literal

from oauthlib.common import Request, _HTTPMethod

from ..request_validator import RequestValidator
from .base import BaseEndpoint

log: Logger

class RevocationEndpoint(BaseEndpoint):
    """Token revocation endpoint.

    Endpoint used by authenticated clients to revoke access and refresh tokens.
    Commonly this will be part of the Authorization Endpoint.
    """

    valid_token_types: tuple[Literal["access_token"], Literal["refresh_token"]]
    valid_request_methods: tuple[Literal["POST"]]
    request_validator: RequestValidator
    supported_token_types: tuple[str, ...]
    enable_jsonp: bool
    def __init__(
        self,
        request_validator: RequestValidator,
        supported_token_types: tuple[str, ...] | None = None,
        enable_jsonp: bool = False,
    ) -> None: ...
    def create_revocation_response(
        self, uri: str, http_method: _HTTPMethod = "POST", body: str | None = None, headers: dict[str, str] | None = None
    ) -> tuple[dict[str, str], str, int]:
        """Revoke supplied access or refresh token.


        The authorization server responds with HTTP status code 200 if the
        token has been revoked successfully or if the client submitted an
        invalid token.

        Note: invalid tokens do not cause an error response since the client
        cannot handle such an error in a reasonable way.  Moreover, the purpose
        of the revocation request, invalidating the particular token, is
        already achieved.

        The content of the response body is ignored by the client as all
        necessary information is conveyed in the response code.

        An invalid token type hint value is ignored by the authorization server
        and does not influence the revocation response.
        """

    def validate_revocation_request(self, request: Request) -> None:
        """Ensure the request is valid.

        The client constructs the request by including the following parameters
        using the "application/x-www-form-urlencoded" format in the HTTP
        request entity-body:

        token (REQUIRED).  The token that the client wants to get revoked.

        token_type_hint (OPTIONAL).  A hint about the type of the token
        submitted for revocation.  Clients MAY pass this parameter in order to
        help the authorization server to optimize the token lookup.  If the
        server is unable to locate the token using the given hint, it MUST
        extend its search across all of its supported token types.  An
        authorization server MAY ignore this parameter, particularly if it is
        able to detect the token type automatically.  This specification
        defines two such values:

                *  access_token: An Access Token as defined in [RFC6749],
                    `section 1.4`_

                *  refresh_token: A Refresh Token as defined in [RFC6749],
                    `section 1.5`_

                Specific implementations, profiles, and extensions of this
                specification MAY define other values for this parameter using
                the registry defined in `Section 4.1.2`_.

        The client also includes its authentication credentials as described in
        `Section 2.3`_. of [`RFC6749`_].

        .. _`section 1.4`: https://tools.ietf.org/html/rfc6749#section-1.4
        .. _`section 1.5`: https://tools.ietf.org/html/rfc6749#section-1.5
        .. _`section 2.3`: https://tools.ietf.org/html/rfc6749#section-2.3
        .. _`Section 4.1.2`: https://tools.ietf.org/html/draft-ietf-oauth-revocation-11#section-4.1.2
        .. _`RFC6749`: https://tools.ietf.org/html/rfc6749
        """
