from _typeshed import Incomplete
from logging import Logger

from authlib.oidc.core import OpenIDImplicitGrant

log: Logger

class OpenIDHybridGrant(OpenIDImplicitGrant):
    AUTHORIZATION_CODE_LENGTH: int
    RESPONSE_TYPES: Incomplete
    GRANT_TYPE: str
    DEFAULT_RESPONSE_MODE: str
    def generate_authorization_code(self):
        """ "The method to generate "code" value for authorization code data.
        Developers may rewrite this method, or customize the code length with::

            class MyAuthorizationCodeGrant(AuthorizationCodeGrant):
                AUTHORIZATION_CODE_LENGTH = 32  # default is 48
        """

    def save_authorization_code(self, code, request) -> None:
        """Save authorization_code for later use. Developers MUST implement
        it in subclass. Here is an example::

            def save_authorization_code(self, code, request):
                client = request.client
                auth_code = AuthorizationCode(
                    code=code,
                    client_id=client.client_id,
                    redirect_uri=request.payload.redirect_uri,
                    scope=request.payload.scope,
                    nonce=request.payload.data.get("nonce"),
                    user_id=request.user.id,
                )
                auth_code.save()
        """

    def validate_authorization_request(self): ...
    def create_granted_params(self, grant_user): ...
