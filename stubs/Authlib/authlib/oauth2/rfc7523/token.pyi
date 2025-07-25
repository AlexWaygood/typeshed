from _typeshed import Incomplete

class JWTBearerTokenGenerator:
    """A JSON Web Token formatted bearer token generator for jwt-bearer grant type.
    This token generator can be registered into authorization server::

        authorization_server.register_token_generator(
            "urn:ietf:params:oauth:grant-type:jwt-bearer",
            JWTBearerTokenGenerator(private_rsa_key),
        )

    In this way, we can generate the token into JWT format. And we don't have to
    save this token into database, since it will be short time valid. Consider to
    rewrite ``JWTBearerGrant.save_token``::

        class MyJWTBearerGrant(JWTBearerGrant):
            def save_token(self, token):
                pass

    :param secret_key: private RSA key in bytes, JWK or JWK Set.
    :param issuer: a string or URI of the issuer
    :param alg: ``alg`` to use in JWT
    """

    DEFAULT_EXPIRES_IN: int
    secret_key: Incomplete
    issuer: Incomplete
    alg: Incomplete
    def __init__(self, secret_key, issuer=None, alg: str = "RS256") -> None: ...
    @staticmethod
    def get_allowed_scope(client, scope): ...
    @staticmethod
    def get_sub_value(user):
        """Return user's ID as ``sub`` value in token payload. For instance::

        @staticmethod
        def get_sub_value(user):
            return str(user.id)
        """

    def get_token_data(self, grant_type, client, expires_in, user=None, scope=None): ...
    def generate(self, grant_type, client, user=None, scope=None, expires_in=None):
        """Generate a bearer token for OAuth 2.0 authorization token endpoint.

        :param client: the client that making the request.
        :param grant_type: current requested grant_type.
        :param user: current authorized user.
        :param expires_in: if provided, use this value as expires_in.
        :param scope: current requested scope.
        :return: Token dict
        """

    def __call__(self, grant_type, client, user=None, scope=None, expires_in=None, include_refresh_token: bool = True): ...
