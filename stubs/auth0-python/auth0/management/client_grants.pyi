from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class ClientGrants:
    """Auth0 client grants endpoints

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
    def all(
        self,
        audience: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
        client_id: str | None = None,
        allow_any_organization: bool | None = None,
    ) -> dict[str, Incomplete]:
        """Retrieves all client grants.

        Args:
            audience (str, optional): URL encoded audience of a Resource Server
                to filter.

            page (int, optional): The result's page number (zero based). When not set,
                the default value is up to the server.

            per_page (int, optional): The amount of entries per page. When not set,
                the default value is up to the server.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to False.

            client_id (string, optional): The id of a client to filter.

            allow_any_organization (bool, optional): Optional filter on allow_any_organization.

        See: https://auth0.com/docs/api/management/v2#!/Client_Grants/get_client_grants
        """

    async def all_async(
        self,
        audience: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
        client_id: str | None = None,
        allow_any_organization: bool | None = None,
    ) -> dict[str, Incomplete]: ...
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Creates a client grant.

        Args:
           body (dict): Attributes for the new client grant.

        See: https://auth0.com/docs/api/management/v2#!/Client_Grants/post_client_grants
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete(self, id: str):
        """Deletes a client grant.

        Args:
           id (str): Id of client grant to delete.

        See: https://auth0.com/docs/api/management/v2#!/Client_Grants/delete_client_grants_by_id
        """

    async def delete_async(self, id: str): ...
    def update(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Modifies a client grant.

        Args:
           id (str): The id of the client grant to modify.

           body (dict): Attributes to update.

        See: https://auth0.com/docs/api/management/v2#!/Client_Grants/patch_client_grants_by_id
        """

    async def update_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_organizations(
        self,
        id: str,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
        from_param: str | None = None,
        take: int | None = None,
    ) -> dict[str, Incomplete]:
        """Get the organizations associated to a client grant.

        Args:
            id (str): Id of client grant.

            page (int, optional): The result's page number (zero based). When not set,
                the default value is up to the server.

            per_page (int, optional): The amount of entries per page. When not set,
                the default value is up to the server.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to False.

            from_param (str, optional): Id to start retrieving entries. You can
                limit the amount of entries using the take parameter.

            take (int, optional): The total amount of entries to retrieve when
                using the from parameter. When not set, the default value is up to the server.
        """

    async def get_organizations_async(
        self,
        id: str,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
        from_param: str | None = None,
        take: int | None = None,
    ) -> dict[str, Incomplete]: ...
