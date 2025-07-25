from _typeshed import Incomplete

from auth0.rest import RestClient
from auth0.types import TimeoutType

class Users:
    """Users client.

    Args:
        domain (str): The domain of your Auth0 tenant
        telemetry (bool, optional): Enable or disable telemetry (defaults to True)
        timeout (float or tuple, optional): Change the requests connect and read timeout. Pass a tuple to specify both values separately or a float to set both to it. (defaults to 5.0 for both)
        protocol (str, optional): Useful for testing. (defaults to 'https')
    """

    domain: str
    protocol: str
    client: RestClient
    def __init__(self, domain: str, telemetry: bool = True, timeout: TimeoutType = 5.0, protocol: str = "https") -> None: ...
    def userinfo(self, access_token: str) -> dict[str, Incomplete]:
        """Returns the user information based on the Auth0 access token.
        This endpoint will work only if openid was granted as a scope for the access_token.

        Args:
            access_token (str): Auth0 access token (obtained during login).

        Returns:
            The user profile.
        """
