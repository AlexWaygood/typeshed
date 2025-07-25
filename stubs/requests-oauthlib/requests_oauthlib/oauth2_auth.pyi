from oauthlib.oauth2 import Client
from requests.auth import AuthBase

class OAuth2(AuthBase):
    """Adds proof of authorization (OAuth2 token) to the request."""

    def __init__(self, client_id=None, client: Client | None = None, token=None) -> None:
        """Construct a new OAuth 2 authorization object.

        :param client_id: Client id obtained during registration
        :param client: :class:`oauthlib.oauth2.Client` to be used. Default is
                       WebApplicationClient which is useful for any
                       hosted application but not mobile or desktop.
        :param token: Token dictionary, must include access_token
                      and token_type.
        """
