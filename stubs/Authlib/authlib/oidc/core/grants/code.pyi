"""authlib.oidc.core.grants.code.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implementation of Authentication using the Authorization Code Flow
per `Section 3.1`_.

.. _`Section 3.1`: http://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth
"""

from logging import Logger

from authlib.oauth2 import OAuth2Request
from authlib.oauth2.rfc6749 import BaseGrant
from authlib.oidc.core import UserInfo

log: Logger

class OpenIDToken:
    def get_jwt_config(self, grant: BaseGrant) -> dict[str, str | int]:
        """Get the JWT configuration for OpenIDCode extension. The JWT
        configuration will be used to generate ``id_token``. Developers
        MUST implement this method in subclass, e.g.::

            def get_jwt_config(self, grant):
                return {
                    "key": read_private_key_file(key_path),
                    "alg": "RS256",
                    "iss": "issuer-identity",
                    "exp": 3600,
                }

        :param grant: AuthorizationCodeGrant instance
        :return: dict
        """

    def generate_user_info(self, user, scope: str) -> UserInfo:
        """Provide user information for the given scope. Developers
        MUST implement this method in subclass, e.g.::

            from authlib.oidc.core import UserInfo


            def generate_user_info(self, user, scope):
                user_info = UserInfo(sub=user.id, name=user.name)
                if "email" in scope:
                    user_info["email"] = user.email
                return user_info

        :param user: user instance
        :param scope: scope of the token
        :return: ``authlib.oidc.core.UserInfo`` instance
        """

    def get_audiences(self, request: OAuth2Request) -> list[str]:
        """Parse `aud` value for id_token, default value is client id. Developers
        MAY rewrite this method to provide a customized audience value.
        """

    def process_token(self, grant: BaseGrant, response) -> dict[str, str | int]: ...
    def __call__(self, grant: BaseGrant) -> None: ...

class OpenIDCode(OpenIDToken):
    """An extension from OpenID Connect for "grant_type=code" request. Developers
    MUST implement the missing methods::

        class MyOpenIDCode(OpenIDCode):
            def get_jwt_config(self, grant):
                return {...}

            def exists_nonce(self, nonce, request):
                return check_if_nonce_in_cache(request.payload.client_id, nonce)

            def generate_user_info(self, user, scope):
                return {...}

    The register this extension with AuthorizationCodeGrant::

        authorization_server.register_grant(
            AuthorizationCodeGrant, extensions=[MyOpenIDCode()]
        )
    """

    require_nonce: bool
    def __init__(self, require_nonce: bool = False) -> None: ...
    def exists_nonce(self, nonce: str, request: OAuth2Request) -> bool:
        """Check if the given nonce is existing in your database. Developers
        MUST implement this method in subclass, e.g.::

            def exists_nonce(self, nonce, request):
                exists = AuthorizationCode.query.filter_by(
                    client_id=request.payload.client_id, nonce=nonce
                ).first()
                return bool(exists)

        :param nonce: A string of "nonce" parameter in request
        :param request: OAuth2Request instance
        :return: Boolean
        """

    def validate_openid_authorization_request(self, grant: BaseGrant, redirect_uri) -> None: ...
    def __call__(self, grant: BaseGrant) -> None: ...
