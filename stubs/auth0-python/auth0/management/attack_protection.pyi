from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class AttackProtection:
    """Auth0 attack protection endpoints

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
    def get_breached_password_detection(self) -> dict[str, Incomplete]:
        """Get breached password detection settings.

        Returns the breached password detection settings.

        See: https://auth0.com/docs/api/management/v2#!/Attack_Protection/get_breached_password_detection
        """

    async def get_breached_password_detection_async(self) -> dict[str, Incomplete]: ...
    def update_breached_password_detection(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update breached password detection settings.

        Returns the breached password detection settings.

        Args:

           body (dict): breached password detection settings.

        See: https://auth0.com/docs/api/management/v2#!/Attack_Protection/patch_breached_password_detection
        """

    async def update_breached_password_detection_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_brute_force_protection(self) -> dict[str, Incomplete]:
        """Get the brute force configuration.

        Returns the brute force configuration.

        See: https://auth0.com/docs/api/management/v2#!/Attack_Protection/get_brute_force_protection
        """

    async def get_brute_force_protection_async(self) -> dict[str, Incomplete]: ...
    def update_brute_force_protection(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update the brute force configuration.

        Returns the brute force configuration.

        Args:

           body (dict): updates of the brute force configuration.

        See: https://auth0.com/docs/api/management/v2#!/Attack_Protection/patch_brute_force_protection
        """

    async def update_brute_force_protection_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_suspicious_ip_throttling(self) -> dict[str, Incomplete]:
        """Get the suspicious IP throttling configuration.

        Returns the suspicious IP throttling configuration.

        See: https://auth0.com/docs/api/management/v2#!/Attack_Protection/get_suspicious_ip_throttling
        """

    async def get_suspicious_ip_throttling_async(self) -> dict[str, Incomplete]: ...
    def update_suspicious_ip_throttling(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update the suspicious IP throttling configuration.

        Returns the suspicious IP throttling configuration.

        Args:

           body (dict): updates of the suspicious IP throttling configuration.

        See: https://auth0.com/docs/api/management/v2#!/Attack_Protection/patch_suspicious_ip_throttling
        """

    async def update_suspicious_ip_throttling_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
