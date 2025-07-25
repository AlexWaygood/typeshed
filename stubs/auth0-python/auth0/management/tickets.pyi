from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Tickets:
    """Auth0 tickets endpoints

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

    domain: Incomplete
    protocol: Incomplete
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
    def create_email_verification(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create an email verification ticket.

        Args:
            body (dict): attributes to set on the email verification request.

        See: https://auth0.com/docs/api/v2#!/Tickets/post_email_verification
        """

    async def create_email_verification_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def create_pswd_change(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create password change ticket.

        Args:
            body (dict): attributes to set on the password change request.

        See: https://auth0.com/docs/api/v2#!/Tickets/post_password_change
        """

    async def create_pswd_change_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
