from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Grants:
    """Auth0 grants endpoints

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
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
        extra_params: dict[str, Incomplete] | None = None,
    ):
        """Retrieves all grants.

        Args:
            page (int, optional): The result's page number (zero based). When not set,
               the default value is up to the server.

            per_page (int, optional): The amount of entries per page. When not set,
               the default value is up to the server.

            include_totals (bool, optional): True if the query summary is
               to be included in the result, False otherwise. Defaults to False.

           extra_params (dictionary, optional): The extra parameters to add to
               the request. The page, per_page, and include_totals values
               specified as parameters take precedence over the ones defined here.

        See: https://auth0.com/docs/api/management/v2#!/Grants/get_grants
        """

    async def all_async(
        self,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
        extra_params: dict[str, Incomplete] | None = None,
    ): ...
    def delete(self, id: str):
        """Deletes a grant.

        Args:
           id (str): The id of the grant to delete.

        See: https://auth0.com/docs/api/management/v2#!/Grants/delete_grants_by_id
        """

    async def delete_async(self, id: str): ...
