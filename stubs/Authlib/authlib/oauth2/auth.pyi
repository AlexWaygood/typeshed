from _typeshed import Incomplete

def encode_client_secret_basic(client, method, uri, headers, body): ...
def encode_client_secret_post(client, method, uri, headers, body): ...
def encode_none(client, method, uri, headers, body): ...

class ClientAuth:
    """Attaches OAuth Client Information to HTTP requests.

    :param client_id: Client ID, which you get from client registration.
    :param client_secret: Client Secret, which you get from registration.
    :param auth_method: Client auth method for token endpoint. The supported
        methods for now:

        * client_secret_basic (default)
        * client_secret_post
        * none
    """

    DEFAULT_AUTH_METHODS: Incomplete
    client_id: Incomplete
    client_secret: Incomplete
    auth_method: Incomplete
    def __init__(self, client_id, client_secret, auth_method=None) -> None: ...
    def prepare(self, method, uri, headers, body): ...

class TokenAuth:
    """Attach token information to HTTP requests.

    :param token: A dict or OAuth2Token instance of an OAuth 2.0 token
    :param token_placement: The placement of the token, default is ``header``,
        available choices:

        * header (default)
        * body
        * uri
    """

    DEFAULT_TOKEN_TYPE: str
    SIGN_METHODS: Incomplete
    token: Incomplete
    token_placement: Incomplete
    client: Incomplete
    hooks: Incomplete
    def __init__(self, token, token_placement: str = "header", client=None) -> None: ...
    def set_token(self, token) -> None: ...
    def prepare(self, uri, headers, body): ...
    def __del__(self) -> None: ...
