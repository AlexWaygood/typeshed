from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class ClientCredentials:
    """Auth0 client credentials endpoints.

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
    def all(self, client_id: str) -> list[dict[str, Incomplete]]:
        """Get a list of credentials associated with a client.

        Args:
            client_id (string): The id of a client that owns the credentials.

        See: https://auth0.com/docs/api/management/v2#!/Client_Credentials/get_client_credentials
        """

    async def all_async(self, client_id: str) -> list[dict[str, Incomplete]]: ...
    def get(self, client_id: str, id: str) -> dict[str, Incomplete]:
        """Retrieve a specified client credential.

        Args:
            client_id (string): The id of a client that owns the credential.

            id (string): The id of the credential.

        See: https://auth0.com/docs/api/management/v2#!/Client_Credentials/get_client_credentials_by_id
        """

    async def get_async(self, client_id: str, id: str) -> dict[str, Incomplete]: ...
    def create(self, client_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create a credential on a client.

        Args:
            client_id (string): The id of a client to create the credential for.

        See: https://auth0.com/docs/api/management/v2#!/Client_Credentials/post_client_credentials
        """

    async def create_async(self, client_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete(self, client_id: str, id: str) -> dict[str, Incomplete]:
        """Delete a client's credential.

        Args:
           id (str): The id of credential to delete.

        See: https://auth0.com/docs/api/management/v2#!/Client_Credentials/delete_client_credentials_by_id
        """

    async def delete_async(self, client_id: str, id: str) -> dict[str, Incomplete]: ...
