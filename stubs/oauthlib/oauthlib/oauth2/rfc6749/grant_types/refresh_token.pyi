"""
oauthlib.oauth2.rfc6749.grant_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from collections.abc import Iterable
from logging import Logger

from oauthlib.common import Request

from ..request_validator import RequestValidator
from ..tokens import TokenBase
from .base import GrantTypeBase, _AuthValidator, _TokenValidator

log: Logger

class RefreshTokenGrant(GrantTypeBase):
    """`Refresh token grant`_

    .. _`Refresh token grant`: https://tools.ietf.org/html/rfc6749#section-6
    """

    def __init__(
        self,
        request_validator: RequestValidator | None = None,
        issue_new_refresh_tokens: bool = True,
        *,
        post_auth: Iterable[_AuthValidator] | None = None,
        post_token: Iterable[_TokenValidator] | None = None,
        pre_auth: Iterable[_AuthValidator] | None = None,
        pre_token: Iterable[_TokenValidator] | None = None,
        **kwargs,
    ) -> None: ...
    def create_token_response(self, request: Request, token_handler: TokenBase) -> tuple[dict[str, str], str, int | None]:
        """Create a new access token from a refresh_token.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param token_handler: A token handler instance, for example of type
                              oauthlib.oauth2.BearerToken.

        If valid and authorized, the authorization server issues an access
        token as described in `Section 5.1`_. If the request failed
        verification or is invalid, the authorization server returns an error
        response as described in `Section 5.2`_.

        The authorization server MAY issue a new refresh token, in which case
        the client MUST discard the old refresh token and replace it with the
        new refresh token. The authorization server MAY revoke the old
        refresh token after issuing a new refresh token to the client. If a
        new refresh token is issued, the refresh token scope MUST be
        identical to that of the refresh token included by the client in the
        request.

        .. _`Section 5.1`: https://tools.ietf.org/html/rfc6749#section-5.1
        .. _`Section 5.2`: https://tools.ietf.org/html/rfc6749#section-5.2
        """

    def validate_token_request(self, request: Request) -> None:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """
