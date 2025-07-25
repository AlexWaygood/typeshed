from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Blacklists:
    """Auth0 blacklists endpoints

    Args:
        domain (str): Your Auth0 domain, e.g: 'username.auth0.com'

        token (str): Management API v2 Token

        telemetry (bool, optional): Enable or disable Telemetry
            (defaults to True)

        timeout (float or tuple, optional): Change the requests
            connect and read timeout. Pass a tuple to specify
            both values separately or a float to set both to it.
            (defaults to 5.0 for both)

        protocol (str, optional): Protocol to use when making requests.
            (defaults to "https")

        rest_options (RestClientOptions): Pass an instance of
            RestClientOptions to configure additional RestClient
            options, such as rate-limit retries.
            (defaults to None)
    """

    url: Incomplete
    client: Incomplete
    def __init__(
        self,
        domain: str,
        token: str,
        telemetry: bool = True,
        timeout: TimeoutType = 5.0,
        protocol: str = "https",
        rest_options: RestClientOptions | None = None,
    ) -> None: ...
    def get(self, aud: str | None = None) -> list[dict[str, str]]:
        """Retrieves the jti and aud of all tokens in the blacklist.

        Args:
            aud (str, optional): The JWT's aud claim. The client_id of the
                application for which it was issued.


        See: https://auth0.com/docs/api/management/v2#!/Blacklists/get_tokens
        """

    async def get_async(self, aud: str | None = None) -> list[dict[str, str]]: ...
    def create(self, jti: str, aud: str | None = None) -> dict[str, str]:
        """Adds a token to the blacklist.

        Args:
            jti (str): the jti of the JWT to blacklist.

            aud (str, optional): The JWT's aud claim. The client_id of the
                application for which it was issued.

        See: https://auth0.com/docs/api/management/v2#!/Blacklists/post_tokens
        """

    async def create_async(self, jti: str, aud: str | None = None) -> dict[str, str]: ...
