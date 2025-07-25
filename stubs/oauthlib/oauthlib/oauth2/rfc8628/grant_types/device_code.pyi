from oauthlib.common import Request
from oauthlib.oauth2.rfc6749.grant_types.base import GrantTypeBase
from oauthlib.oauth2.rfc6749.tokens import TokenBase

class DeviceCodeGrant(GrantTypeBase):
    def create_authorization_response(self, request: Request, token_handler: TokenBase) -> tuple[dict[str, str], str, int]:
        """
        Validate the device flow request -> create the access token
        -> persist the token -> return the token.
        """

    def validate_token_request(self, request: Request) -> None:
        """
        Performs the necessary check against the request to ensure
        it's allowed to retrieve a token.
        """

    def create_token_response(self, request: Request, token_handler: TokenBase) -> tuple[dict[str, str], str, int]:
        """Return token or error in json format.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param token_handler: A token handler instance, for example of type
                              oauthlib.oauth2.BearerToken.

        If the access token request is valid and authorized, the
        authorization server issues an access token and optional refresh
        token as described in `Section 5.1`_.  If the request failed client
        authentication or is invalid, the authorization server returns an
        error response as described in `Section 5.2`_.
        .. _`Section 5.1`: https://tools.ietf.org/html/rfc6749#section-5.1
        .. _`Section 5.2`: https://tools.ietf.org/html/rfc6749#section-5.2
        """
