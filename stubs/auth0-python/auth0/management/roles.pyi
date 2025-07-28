from _typeshed import Incomplete
from builtins import list as _list

from ..rest import RestClientOptions
from ..types import TimeoutType

class Roles:
    """Auth0 roles endpoints

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
    def list(
        self, page: int = 0, per_page: int = 25, include_totals: bool = True, name_filter: str | None = None
    ) -> dict[str, Incomplete]:
        """List or search roles.

        Args:
            page (int, optional): The result's page number (zero based). By default,
               retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
               retrieves 25 results per page.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to True.

            name_filter (str, optional): A case-insensitive filter to apply
                to search for roles by name.

        See: https://auth0.com/docs/api/management/v2#!/Roles/get_roles
        """

    async def list_async(
        self, page: int = 0, per_page: int = 25, include_totals: bool = True, name_filter: str | None = None
    ) -> dict[str, Incomplete]: ...
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Creates a new role.

        Args:
            body (dict): the attributes for the role to create.

        See: https://auth0.com/docs/api/v2#!/Roles/post_roles
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get(self, id: str) -> dict[str, Incomplete]:
        """Get a role.

        Args:
            id (str): The id of the role to retrieve.

        See: https://auth0.com/docs/api/management/v2#!/Roles/get_roles_by_id
        """

    async def get_async(self, id: str) -> dict[str, Incomplete]: ...
    def delete(self, id: str):
        """Delete a role.

        Args:
            id (str): The id of the role to delete.

        See: https://auth0.com/docs/api/management/v2#!/Roles/delete_roles_by_id
        """

    async def delete_async(self, id: str): ...
    def update(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update a role with the attributes passed in 'body'

        Args:
            id (str): The id of the role to update.

            body (dict): the attributes to update on the role.

        See: https://auth0.com/docs/api/management/v2#!/Roles/patch_roles_by_id
        """

    async def update_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def list_users(
        self,
        id: str,
        page: int = 0,
        per_page: int = 25,
        include_totals: bool = True,
        from_param: str | None = None,
        take: int | None = None,
    ) -> dict[str, Incomplete]:
        """List the users that have been associated with a given role.

        Args:
            id (str): The role's id.

            page (int, optional): The result's page number (zero based). By default,
               retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
               retrieves 25 results per page.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to True.

            from_param (str, optional): Checkpoint Id from which to begin retrieving results.
                You can limit the number of entries using the take parameter.

            take (int, optional): The total amount of entries to retrieve when
                using the from parameter. When not set, the default value is up to the server.

        See https://auth0.com/docs/api/management/v2#!/Roles/get_role_user
        """

    async def list_users_async(
        self,
        id: str,
        page: int = 0,
        per_page: int = 25,
        include_totals: bool = True,
        from_param: str | None = None,
        take: int | None = None,
    ) -> dict[str, Incomplete]: ...
    def add_users(self, id: str, users: _list[str]) -> dict[str, Incomplete]:
        """Assign users to a role.

        Args:
            id (str): The role's id.

            users (list of str): A list of users ids to add to this role.

        See https://auth0.com/docs/api/management/v2#!/Roles/post_role_users
        """

    async def add_users_async(self, id: str, users: _list[str]) -> dict[str, Incomplete]: ...
    def list_permissions(self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True) -> dict[str, Incomplete]:
        """List the permissions associated to a role.

        Args:
            id (str): The role's id.

            page (int, optional): The result's page number (zero based). By default,
               retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
               retrieves 25 results per page.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to True.

        See https://auth0.com/docs/api/management/v2#!/Roles/get_role_permission
        """

    async def list_permissions_async(
        self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True
    ) -> dict[str, Incomplete]: ...
    def remove_permissions(self, id: str, permissions: _list[dict[str, str]]):
        """Unassociates permissions from a role.

        Args:
            id (str): The role's id.

            permissions (list of str): A list of permission ids to unassociate from the role.

        See https://auth0.com/docs/api/management/v2#!/Roles/delete_role_permission_assignment
        """

    async def remove_permissions_async(self, id: str, permissions: _list[dict[str, str]]): ...
    def add_permissions(self, id: str, permissions: _list[dict[str, str]]) -> dict[str, Incomplete]:
        """Associates permissions with a role.

        Args:
            id (str): The role's id.

            permissions (list of str): A list of permission ids to associate to the role.

        See https://auth0.com/docs/api/management/v2#!/Roles/post_role_permission_assignment
        """

    async def add_permissions_async(self, id: str, permissions: _list[dict[str, str]]) -> dict[str, Incomplete]: ...
