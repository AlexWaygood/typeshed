from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Hooks:
    """Hooks endpoint implementation.

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
        enabled: bool = True,
        fields: list[str] | None = None,
        include_fields: bool = True,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
    ):
        """Retrieves a list of all hooks.

        Args:
            enabled (bool, optional): If provided, retrieves hooks that match
                the value, otherwise all hooks are retrieved.

            fields (list, optional): A list of fields to include or exclude
                (depending on include_fields) from the result, empty to
                retrieve all fields.

            include_fields (bool, optional): True if the fields specified are
                to be included in the result, False otherwise
                (defaults to true).

            page (int, optional): The result's page number (zero based).

            per_page (int, optional): The amount of entries per page.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise.

        See: https://auth0.com/docs/api/management/v2#!/Hooks/get_hooks
        """

    async def all_async(
        self,
        enabled: bool = True,
        fields: list[str] | None = None,
        include_fields: bool = True,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
    ): ...
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Creates a new Hook.

        Args:
            body (dict): Attributes for the newly created hook,
                See: https://auth0.com/docs/api/v2#!/Hooks/post_hooks
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get(self, id: str, fields: list[str] | None = None) -> dict[str, Incomplete]:
        """Retrieves a hook by its ID.

        Args:
            id (str): The id of the hook to retrieve.

            fields (list, optional): A list of fields to include or exclude
                (depending on include_fields) from the result, empty to
                retrieve all fields.

        See: https://auth0.com/docs/api/management/v2#!/Hooks/get_hooks_by_id
        """

    async def get_async(self, id: str, fields: list[str] | None = None) -> dict[str, Incomplete]: ...
    def delete(self, id: str):
        """Deletes a hook.

        Args:
            id (str): The id of the hook to delete.

        See: https://auth0.com/docs/api/management/v2#!/Hooks/delete_hooks_by_id
        """

    async def delete_async(self, id: str): ...
    def update(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Updates an existing hook.

        Args:
            id (str): The id of the hook to modify.

            body (dict): Attributes to modify.

        See: https://auth0.com/docs/api/v2#!/Hooks/patch_hooks_by_id
        """

    async def update_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_secrets(self, id: str) -> dict[str, Incomplete]:
        """Retrieves a hook's secrets.

        Args:
            id (str): The id of the hook to retrieve secrets from.

        See: https://auth0.com/docs/api/management/v2#!/Hooks/get_secrets
        """

    async def get_secrets_async(self, id: str) -> dict[str, Incomplete]: ...
    def add_secrets(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Add one or more secrets for an existing hook.

        Args:
            id (str): The id of the hook to add secrets to.

            body (dict): Dict of key-value pairs where the value must be a string.

        See: https://auth0.com/docs/api/management/v2#!/Hooks/post_secrets
        """

    async def add_secrets_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete_secrets(self, id: str, body: list[str]):
        """Delete one or more existing secrets for an existing hook.

        Args:
            id (str): The id of the hook to add secrets to.

            body (list): List of secret names to delete.

        See: https://auth0.com/docs/api/management/v2#!/Hooks/delete_secrets
        """

    async def delete_secrets_async(self, id: str, body: list[str]): ...
    def update_secrets(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update one or more existing secrets for an existing hook.

        Args:
            id (str): The id of the hook to add secrets to.

            body (dict): Dict of key-value pairs where the value must be a string.

        See: https://auth0.com/docs/api/management/v2#!/Hooks/patch_secrets
        """

    async def update_secrets_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
