"""
oauthlib.openid.connect.core.grant_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from collections.abc import Iterable
from logging import Logger

from oauthlib.common import Request
from oauthlib.oauth2.rfc6749.grant_types.authorization_code import AuthorizationCodeGrant as OAuth2AuthorizationCodeGrant
from oauthlib.oauth2.rfc6749.grant_types.base import _AuthValidator, _TokenValidator
from oauthlib.oauth2.rfc6749.request_validator import RequestValidator as OAuth2RequestValidator

from .base import GrantTypeBase

log: Logger

class AuthorizationCodeGrant(GrantTypeBase):
    proxy_target: OAuth2AuthorizationCodeGrant
    def __init__(
        self,
        request_validator: OAuth2RequestValidator | None = None,
        *,
        post_auth: Iterable[_AuthValidator] | None = None,
        post_token: Iterable[_TokenValidator] | None = None,
        pre_auth: Iterable[_AuthValidator] | None = None,
        pre_token: Iterable[_TokenValidator] | None = None,
        **kwargs,
    ) -> None: ...
    def add_id_token(self, token, token_handler, request: Request):  # type: ignore[override]
        """
        Construct an initial version of id_token, and let the
        request_validator sign or encrypt it.

        The authorization_code version of this method is used to
        retrieve the nonce accordingly to the code storage.
        """
