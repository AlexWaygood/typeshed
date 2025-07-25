from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class RulesConfigs:
    """RulesConfig endpoint implementation.

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
    def all(self) -> list[dict[str, Incomplete]]:
        """Lists the config variable keys for rules.

        See: https://auth0.com/docs/api/management/v2#!/Rules_Configs/get_rules_configs
        """

    async def all_async(self) -> list[dict[str, Incomplete]]: ...
    def unset(self, key: str):
        """Removes the rules config for a given key.

        Args:
            key (str): rules config key to remove.

        See: https://auth0.com/docs/api/management/v2#!/Rules_Configs/delete_rules_configs_by_key
        """

    async def unset_async(self, key: str): ...
    def set(self, key: str, value: str) -> dict[str, Incomplete]:
        """Sets the rules config for a given key.

        Args:
            key (str): rules config key to set.

            value (str): value to set for the rules config key.

        See: https://auth0.com/docs/api/management/v2#!/Rules_Configs/put_rules_configs_by_key
        """

    async def set_async(self, key: str, value: str) -> dict[str, Incomplete]: ...
