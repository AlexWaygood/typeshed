from _typeshed import Incomplete
from typing import Final

from auth0.rest import RestClient
from auth0.types import RequestData

UNKNOWN_ERROR: Final[str]

class AuthenticationBase:
    """Base authentication object providing simple REST methods.

    Args:
        domain (str): The domain of your Auth0 tenant
        client_id (str): Your application's client ID
        client_secret (str, optional): Your application's client secret
        client_assertion_signing_key (str, optional): Private key used to sign the client assertion JWT.
        client_assertion_signing_alg (str, optional): Algorithm used to sign the client assertion JWT (defaults to 'RS256').
        telemetry (bool, optional): Enable or disable telemetry (defaults to True)
        timeout (float or tuple, optional): Change the requests connect and read timeout. Pass a tuple to specify both values separately or a float to set both to it. (defaults to 5.0 for both)
        protocol (str, optional): Useful for testing. (defaults to 'https')
    """

    domain: str
    client_id: str
    client_secret: str | None
    client_assertion_signing_key: str | None
    client_assertion_signing_alg: str | None
    protocol: str
    client: RestClient
    def __init__(
        self,
        domain: str,
        client_id: str,
        client_secret: str | None = None,
        client_assertion_signing_key: str | None = None,
        client_assertion_signing_alg: str | None = None,
        telemetry: bool = True,
        timeout: float | tuple[float, float] = 5.0,
        protocol: str = "https",
    ) -> None: ...
    def post(self, url: str, data: RequestData | None = None, headers: dict[str, str] | None = None): ...
    def authenticated_post(self, url: str, data: dict[str, Incomplete], headers: dict[str, str] | None = None): ...
    def get(self, url: str, params: dict[str, Incomplete] | None = None, headers: dict[str, str] | None = None): ...
