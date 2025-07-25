from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class DeviceCredentials:
    """Auth0 connection endpoints

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
    def get(
        self,
        user_id: str,
        client_id: str,
        type: str,
        fields: list[str] | None = None,
        include_fields: bool = True,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
    ):
        """List device credentials.

        Args:
            user_id (str): The user_id of the devices to retrieve.

            client_id (str): The client_id of the devices to retrieve.

            type (str): The type of credentials (public_key, refresh_token).

            fields (list, optional): A list of fields to include or exclude
                (depending on include_fields) from the result. Leave empty to
                retrieve all fields.

            include_fields (bool, optional): True if the fields specified are
                to be included in the result, False otherwise. Defaults to True.

            page (int, optional): Page index of the results to return. First page is 0.

            per_page (int, optional): Number of results per page.

            include_totals (bool, optional): True to return results inside an object
                that contains the total result count (True) or as a direct array of
                results (False, default).

        See: https://auth0.com/docs/api/management/v2#!/Device_Credentials/get_device_credentials
        """

    async def get_async(
        self,
        user_id: str,
        client_id: str,
        type: str,
        fields: list[str] | None = None,
        include_fields: bool = True,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
    ): ...
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create a device public key.

        Args:
            body (dict): parameters for creating the public key (e.g: type,
                device_name, client_id, etc).

        See: https://auth0.com/docs/api/v2#!/Device_Credentials/post_device_credentials
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete(self, id: str):
        """Delete credential.

        Args:
            id (str):  The id of the credential to delete.

        See: https://auth0.com/docs/api/management/v2#!/Device_Credentials/delete_device_credentials_by_id
        """

    async def delete_async(self, id: str): ...
