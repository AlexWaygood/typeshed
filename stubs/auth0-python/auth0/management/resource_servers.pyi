from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class ResourceServers:
    """Auth0 resource servers endpoints

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
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create a new resource server.

        Args:
           body (dict): Attributes for the new resource Server.

        See: https://auth0.com/docs/api/management/v2#!/Resource_Servers/post_resource_servers
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_all(self, page: int | None = None, per_page: int | None = None, include_totals: bool = False):
        """Retrieves all resource servers

        Args:
            page (int, optional): The result's page number (zero based). When not set,
              the default value is up to the server.

            per_page (int, optional): The amount of entries per page. When not set,
              the default value is up to the server.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to False.


        See: https://auth0.com/docs/api/management/v2#!/Resource_Servers/get_resource_servers
        """

    async def get_all_async(self, page: int | None = None, per_page: int | None = None, include_totals: bool = False): ...
    def get(self, id: str) -> dict[str, Incomplete]:
        """Retrieves a resource server by its id.

        Args:
           id (str): id of the resource server to get.


        See: https://auth0.com/docs/api/management/v2#!/Resource_Servers/get_resource_servers_by_id
        """

    async def get_async(self, id: str) -> dict[str, Incomplete]: ...
    def delete(self, id: str):
        """Deletes a resource server.

        Args:
           id (str): Id of resource server to delete.


        See: https://auth0.com/docs/api/management/v2#!/Resource_Servers/delete_resource_servers_by_id
        """

    async def delete_async(self, id: str): ...
    def update(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Modifies a resource server.

        Args:
           id (str): The id of the resource server to update.

           body (dict): Attributes to modify.

        See: https://auth0.com/docs/api/management/v2#!/Resource_Servers/patch_resource_servers_by_id
        """

    async def update_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
