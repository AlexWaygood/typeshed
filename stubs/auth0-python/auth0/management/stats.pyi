from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Stats:
    """Auth0 stats endpoints

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
    def active_users(self) -> int:
        """Gets the active users count (logged in during the last 30 days).

        Returns: An integer.

        See: https://auth0.com/docs/api/management/v2#!/Stats/get_active_users
        """

    async def active_users_async(self) -> int: ...
    def daily_stats(self, from_date: str | None = None, to_date: str | None = None) -> list[dict[str, Incomplete]]:
        """Gets the daily stats for a particular period.

        Args:
           from_date (str, optional): The first day of the period (inclusive) in
              YYYYMMDD format.

           to_date (str, optional): The last day of the period (inclusive) in
              YYYYMMDD format.

        See: https://auth0.com/docs/api/management/v2#!/Stats/get_daily
        """

    async def daily_stats_async(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Incomplete]]: ...
