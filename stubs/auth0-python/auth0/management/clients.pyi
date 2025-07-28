from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Clients:
    """Auth0 applications endpoints

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
        fields: list[str] | None = None,
        include_fields: bool = True,
        page: int | None = None,
        per_page: int | None = None,
        extra_params: dict[str, Incomplete] | None = None,
    ) -> list[dict[str, Incomplete]]:
        """Retrieves a list of all the applications.

        Important: The client_secret and encryption_key attributes can only be
        retrieved with the read:client_keys scope.

        Args:
           fields (list of str, optional): A list of fields to include or
              exclude from the result (depending on include_fields). Leave empty to
              retrieve all fields.

           include_fields (bool, optional): True if the fields specified are
              to be included in the result, False otherwise. Defaults to True.

           page (int, optional): The result's page number (zero based). When not set,
              the default value is up to the server.

           per_page (int, optional): The amount of entries per page. When not set,
              the default value is up to the server.

           extra_params (dictionary, optional): The extra parameters to add to
             the request. The fields, include_fields, page and per_page values
             specified as parameters take precedence over the ones defined here.

        See: https://auth0.com/docs/api/management/v2#!/Clients/get_clients
        """

    async def all_async(
        self,
        fields: list[str] | None = None,
        include_fields: bool = True,
        page: int | None = None,
        per_page: int | None = None,
        extra_params: dict[str, Incomplete] | None = None,
    ) -> list[dict[str, Incomplete]]: ...
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create a new application.

        Args:
           body (dict): Attributes for the new application.

        See: https://auth0.com/docs/api/v2#!/Clients/post_clients
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get(self, id: str, fields: list[str] | None = None, include_fields: bool = True) -> dict[str, Incomplete]:
        """Retrieves an application by its id.

        Important: The client_secret, encryption_key and signing_keys
        attributes can only be retrieved with the read:client_keys scope.

        Args:
           id (str): Id of the application to get.

           fields (list of str, optional): A list of fields to include or
              exclude from the result (depending on include_fields). Leave empty to
              retrieve all fields.

           include_fields (bool, optional): True if the fields specified are
              to be included in the result, False otherwise. Defaults to True.

        See: https://auth0.com/docs/api/management/v2#!/Clients/get_clients_by_id
        """

    async def get_async(self, id: str, fields: list[str] | None = None, include_fields: bool = True) -> dict[str, Incomplete]: ...
    def delete(self, id: str):
        """Deletes an application and all its related assets.

        Args:
           id (str): Id of application to delete.

        See: https://auth0.com/docs/api/management/v2#!/Clients/delete_clients_by_id
        """

    async def delete_async(self, id: str): ...
    def update(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Modifies an application.

        Important: The client_secret, encryption_key and signing_keys
        attributes can only be updated with the update:client_keys scope.

        Args:
           id (str): Client ID of the application.

           body (dict): Attributes to modify.

        See: https://auth0.com/docs/api/management/v2#!/Clients/patch_clients_by_id
        """

    async def update_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def rotate_secret(self, id: str) -> dict[str, Incomplete]:
        """Rotate a client secret. The generated secret is NOT base64 encoded.

        Args:
           id (str): Client ID of the application.

        See: https://auth0.com/docs/api/management/v2#!/Clients/post_rotate_secret
        """

    async def rotate_secret_async(self, id: str) -> dict[str, Incomplete]: ...
