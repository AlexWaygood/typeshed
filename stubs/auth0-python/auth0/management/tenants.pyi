from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Tenants:
    """Auth0 tenants endpoints

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
    def get(self, fields: list[str] | None = None, include_fields: bool = True) -> dict[str, Incomplete]:
        """Get tenant settings.

        Args:
           fields (list of str, optional): A list of fields to include or
              exclude from the result (depending on include_fields). Leave empty to
              retrieve all fields.

           include_fields (bool, optional): True if the fields specified are
              to be included in the result, False otherwise. Defaults to True.

        See: https://auth0.com/docs/api/management/v2#!/Tenants/get_settings
        """

    async def get_async(self, fields: list[str] | None = None, include_fields: bool = True) -> dict[str, Incomplete]: ...
    def update(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update tenant settings.

        Args:
            body (dict): the attributes to update in the tenant.

        See: https://auth0.com/docs/api/v2#!/Tenants/patch_settings
        """

    async def update_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
