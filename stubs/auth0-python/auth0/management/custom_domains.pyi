from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class CustomDomains:
    """Auth0 custom domains endpoints

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
        """Retrieves all custom domains.

        See: https://auth0.com/docs/api/management/v2#!/Custom_Domains/get_custom_domains
        """

    async def all_async(self) -> list[dict[str, Incomplete]]: ...
    def get(self, id: str) -> dict[str, Incomplete]:
        """Retrieves custom domain.

        See: https://auth0.com/docs/api/management/v2#!/Custom_Domains/get_custom_domains_by_id
        """

    async def get_async(self, id: str) -> dict[str, Incomplete]: ...
    def delete(self, id: str):
        """Deletes a grant.

        Args:
           id (str): The id of the custom domain to delete.

        See: https://auth0.com/docs/api/management/v2#!/Custom_Domains/delete_custom_domains_by_id
        """

    async def delete_async(self, id: str): ...
    def create_new(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Configure a new custom domain.

        Args:
           body (str): The domain, tye and verification method in json.

        See: https://auth0.com/docs/api/management/v2#!/Custom_Domains/post_custom_domains
        """

    async def create_new_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def verify(self, id: str) -> dict[str, Incomplete]:
        """Verify a custom domain.

        Args:
           id (str): The id of the custom domain to delete.

        See: https://auth0.com/docs/api/management/v2#!/Custom_Domains/post_verify
        """

    async def verify_async(self, id: str) -> dict[str, Incomplete]: ...
