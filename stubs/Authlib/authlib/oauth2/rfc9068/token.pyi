from _typeshed import Incomplete

from authlib.oauth2.rfc6750 import BearerTokenGenerator

class JWTBearerTokenGenerator(BearerTokenGenerator):
    """A JWT formatted access token generator.

    :param issuer: The issuer identifier. Will appear in the JWT ``iss`` claim.

    :param \\\\*\\\\*kwargs: Other parameters are inherited from
        :class:`~authlib.oauth2.rfc6750.token.BearerTokenGenerator`.

    This token generator can be registered into the authorization server::

        class MyJWTBearerTokenGenerator(JWTBearerTokenGenerator):
            def get_jwks(self): ...

            def get_extra_claims(self, client, grant_type, user, scope): ...


        authorization_server.register_token_generator(
            "default",
            MyJWTBearerTokenGenerator(
                issuer="https://authorization-server.example.org"
            ),
        )
    """

    issuer: Incomplete
    alg: Incomplete
    def __init__(self, issuer, alg: str = "RS256", refresh_token_generator=None, expires_generator=None) -> None: ...
    def get_jwks(self) -> None:
        """Return the JWKs that will be used to sign the JWT access token.
        Developers MUST re-implement this method::

            def get_jwks(self):
                return load_jwks("jwks.json")
        """

    def get_extra_claims(self, client, grant_type, user, scope):
        """Return extra claims to add in the JWT access token. Developers MAY
        re-implement this method to add identity claims like the ones in
        :ref:`specs/oidc` ID Token, or any other arbitrary claims::

            def get_extra_claims(self, client, grant_type, user, scope):
                return generate_user_info(user, scope)
        """

    def get_audiences(self, client, user, scope) -> str | list[str]:
        """Return the audience for the token. By default this simply returns
        the client ID. Developers MAY re-implement this method to add extra
        audiences::

            def get_audiences(self, client, user, scope):
                return [
                    client.get_client_id(),
                    resource_server.get_id(),
                ]
        """

    def get_acr(self, user) -> str | None:
        """Authentication Context Class Reference.
        Returns a user-defined case sensitive string indicating the class of
        authentication the used performed. Token audience may refuse to give access to
        some resources if some ACR criteria are not met.
        :ref:`specs/oidc` defines one special value: ``0`` means that the user
        authentication did not respect `ISO29115`_ level 1, and will be refused monetary
        operations. Developers MAY re-implement this method::

            def get_acr(self, user):
                if user.insecure_session():
                    return "0"
                return "urn:mace:incommon:iap:silver"

        .. _ISO29115: https://www.iso.org/standard/45138.html
        """

    def get_auth_time(self, user) -> int | None:
        """User authentication time.
        Time when the End-User authentication occurred. Its value is a JSON number
        representing the number of seconds from 1970-01-01T0:0:0Z as measured in UTC
        until the date/time. Developers MAY re-implement this method::

            def get_auth_time(self, user):
                return datetime.timestamp(user.get_auth_time())
        """

    def get_amr(self, user) -> list[str] | None:
        """Authentication Methods References.
        Defined by :ref:`specs/oidc` as an option list of user-defined case-sensitive
        strings indication which authentication methods have been used to authenticate
        the user. Developers MAY re-implement this method::

            def get_amr(self, user):
                return ["2FA"] if user.has_2fa_enabled() else []
        """

    def get_jti(self, client, grant_type, user, scope) -> str:
        """JWT ID.
        Create an unique identifier for the token. Developers MAY re-implement
        this method::

            def get_jti(self, client, grant_type, user scope):
                return generate_random_string(16)
        """
    # Override seems safe, but mypy doesn't like that it's a callabe protocol in the base
    def access_token_generator(self, client, grant_type, user, scope): ...  # type: ignore[override]
