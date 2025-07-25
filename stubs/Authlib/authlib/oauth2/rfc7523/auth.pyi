from _typeshed import Incomplete

class ClientSecretJWT:
    """Authentication method for OAuth 2.0 Client. This authentication
    method is called ``client_secret_jwt``, which is using ``client_id``
    and ``client_secret`` constructed with JWT to identify a client.

    Here is an example of use ``client_secret_jwt`` with Requests Session::

        from authlib.integrations.requests_client import OAuth2Session

        token_endpoint = "https://example.com/oauth/token"
        session = OAuth2Session(
            "your-client-id",
            "your-client-secret",
            token_endpoint_auth_method="client_secret_jwt",
        )
        session.register_client_auth_method(ClientSecretJWT(token_endpoint))
        session.fetch_token(token_endpoint)

    :param token_endpoint: A string URL of the token endpoint
    :param claims: Extra JWT claims
    :param headers: Extra JWT headers
    :param alg: ``alg`` value, default is HS256
    """

    name: str
    alg: str
    token_endpoint: Incomplete
    claims: Incomplete
    headers: Incomplete
    def __init__(self, token_endpoint=None, claims=None, headers=None, alg=None) -> None: ...
    def sign(self, auth, token_endpoint): ...
    def __call__(self, auth, method, uri, headers, body): ...

class PrivateKeyJWT(ClientSecretJWT):
    """Authentication method for OAuth 2.0 Client. This authentication
    method is called ``private_key_jwt``, which is using ``client_id``
    and ``private_key`` constructed with JWT to identify a client.

    Here is an example of use ``private_key_jwt`` with Requests Session::

        from authlib.integrations.requests_client import OAuth2Session

        token_endpoint = "https://example.com/oauth/token"
        session = OAuth2Session(
            "your-client-id",
            "your-client-private-key",
            token_endpoint_auth_method="private_key_jwt",
        )
        session.register_client_auth_method(PrivateKeyJWT(token_endpoint))
        session.fetch_token(token_endpoint)

    :param token_endpoint: A string URL of the token endpoint
    :param claims: Extra JWT claims
    :param headers: Extra JWT headers
    :param alg: ``alg`` value, default is RS256
    """

    name: str
    alg: str
    def sign(self, auth, token_endpoint): ...
