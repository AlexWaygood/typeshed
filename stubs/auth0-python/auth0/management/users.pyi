from _typeshed import Incomplete
from builtins import list as _list

from ..rest import RestClientOptions
from ..types import TimeoutType

class Users:
    """Auth0 users endpoints

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
        self,
        page: int = 0,
        per_page: int = 25,
        sort: str | None = None,
        connection: str | None = None,
        q: str | None = None,
        search_engine: str | None = None,
        include_totals: bool = True,
        fields: _list[str] | None = None,
        include_fields: bool = True,
    ) -> dict[str, Incomplete]:
        """List or search users.

        Args:
            page (int, optional): The result's page number (zero based). By default,
               retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
               retrieves 25 results per page.

            sort (str, optional): The field to use for sorting.
                1 == ascending and -1 == descending. (e.g: email:1)
                When not set, the default value is up to the server.

            connection (str, optional): Connection filter.

            q (str, optional): Query in Lucene query string syntax. Only fields
                in app_metadata, user_metadata or the normalized user profile
                are searchable.

            search_engine (str, optional): The version of the search_engine to use
                when querying for users. Will default to the latest version available.
                See: https://auth0.com/docs/users/search.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to True.

            fields (list of str, optional): A list of fields to include or
                exclude from the result (depending on include_fields). Leave empty to
                retrieve all fields.

            include_fields (bool, optional): True if the fields specified are
                to be include in the result, False otherwise. Defaults to True.

        See: https://auth0.com/docs/api/management/v2#!/Users/get_users
        """

    async def list_async(
        self,
        page: int = 0,
        per_page: int = 25,
        sort: str | None = None,
        connection: str | None = None,
        q: str | None = None,
        search_engine: str | None = None,
        include_totals: bool = True,
        fields: _list[str] | None = None,
        include_fields: bool = True,
    ) -> dict[str, Incomplete]: ...
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Creates a new user.

        Args:
            body (dict): the attributes to set on the user to create.

        See: https://auth0.com/docs/api/v2#!/Users/post_users
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get(self, id: str, fields: _list[str] | None = None, include_fields: bool = True) -> dict[str, Incomplete]:
        """Get a user.

        Args:
            id (str): The user_id of the user to retrieve.

            fields (list of str, optional): A list of fields to include or
                exclude from the result (depending on include_fields). Leave empty to
                retrieve all fields.

            include_fields (bool, optional): True if the fields specified are
                to be included in the result, False otherwise. Defaults to True.

        See: https://auth0.com/docs/api/management/v2#!/Users/get_users_by_id
        """

    async def get_async(
        self, id: str, fields: _list[str] | None = None, include_fields: bool = True
    ) -> dict[str, Incomplete]: ...
    def delete(self, id: str):
        """Delete a user.

        Args:
            id (str): The user_id of the user to delete.

        See: https://auth0.com/docs/api/management/v2#!/Users/delete_users_by_id
        """

    async def delete_async(self, id: str): ...
    def update(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update a user with the attributes passed in 'body'

        Args:
            id (str): The user_id of the user to update.

            body (dict): The attributes of the user to update.

        See: https://auth0.com/docs/api/v2#!/Users/patch_users_by_id
        """

    async def update_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def list_organizations(
        self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True
    ) -> dict[str, Incomplete]:
        """List the organizations that the user is member of.

        Args:
            id (str): The user's id.

            page (int, optional): The result's page number (zero based). By default,
               retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
               retrieves 25 results per page.

            include_totals (bool, optional): True if the query summary is
               to be included in the result, False otherwise. Defaults to True.

        See https://auth0.com/docs/api/management/v2#!/Users/get_organizations
        """

    async def list_organizations_async(
        self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True
    ) -> dict[str, Incomplete]: ...
    def list_roles(self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True) -> dict[str, Incomplete]:
        """List the roles associated with a user.

        Args:
            id (str): The user's id.

            page (int, optional): The result's page number (zero based). By default,
               retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
               retrieves 25 results per page.

            include_totals (bool, optional): True if the query summary is
               to be included in the result, False otherwise. Defaults to True.

        See https://auth0.com/docs/api/management/v2#!/Users/get_user_roles
        """

    async def list_roles_async(
        self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True
    ) -> dict[str, Incomplete]: ...
    def remove_roles(self, id: str, roles: _list[str]):
        """Removes an array of roles from a user.

        Args:
            id (str): The user's id.

            roles (list of str): A list of roles ids to unassociate from the user.

        See https://auth0.com/docs/api/management/v2#!/Users/delete_user_roles
        """

    async def remove_roles_async(self, id: str, roles: _list[str]): ...
    def add_roles(self, id: str, roles: _list[str]) -> dict[str, Incomplete]:
        """Associate an array of roles with a user.

        Args:
            id (str): The user's id.

            roles (list of str): A list of roles ids to associated with the user.

        See https://auth0.com/docs/api/management/v2#!/Users/post_user_roles
        """

    async def add_roles_async(self, id: str, roles: _list[str]) -> dict[str, Incomplete]: ...
    def list_permissions(self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True) -> dict[str, Incomplete]:
        """List the permissions associated to the user.

        Args:
            id (str): The user's id.

            page (int, optional): The result's page number (zero based). By default,
               retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
               retrieves 25 results per page.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to True.

        See https://auth0.com/docs/api/management/v2#!/Users/get_permissions
        """

    async def list_permissions_async(
        self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True
    ) -> dict[str, Incomplete]: ...
    def remove_permissions(self, id: str, permissions: _list[str]):
        """Removes permissions from a user.

        Args:
            id (str): The user's id.

            permissions (list of str): A list of permission ids to unassociate from the user.

        See https://auth0.com/docs/api/management/v2#!/Users/delete_permissions
        """

    async def remove_permissions_async(self, id: str, permissions: _list[str]): ...
    def add_permissions(self, id: str, permissions: _list[str]) -> dict[str, Incomplete]:
        """Assign permissions to a user.

        Args:
            id (str): The user's id.

            permissions (list of str): A list of permission ids to associated with the user.

        See https://auth0.com/docs/api/management/v2#!/Users/post_permissions
        """

    async def add_permissions_async(self, id: str, permissions: _list[str]) -> dict[str, Incomplete]: ...
    def delete_multifactor(self, id: str, provider: str):
        """Delete a user's multifactor provider.

        Args:
            id (str): The user's id.

            provider (str): The multifactor provider. Supported values 'duo'
                or 'google-authenticator'.

        See: https://auth0.com/docs/api/management/v2#!/Users/delete_multifactor_by_provider
        """

    async def delete_multifactor_async(self, id: str, provider: str): ...
    def delete_authenticators(self, id: str):
        """Delete a user's MFA enrollments.

        Args:
            id (str): The user's id.

        See: https://auth0.com/docs/api/management/v2#!/Users/delete_authenticators
        """

    async def delete_authenticators_async(self, id: str): ...
    def unlink_user_account(self, id: str, provider: str, user_id: str):
        """Unlink a user account

        Args:
            id (str): The user_id of the user identity.

            provider (str): The type of identity provider (e.g: facebook).

            user_id (str): The unique identifier for the user for the identity.

        See: https://auth0.com/docs/api/management/v2#!/Users/delete_user_identity_by_user_id
        """

    async def unlink_user_account_async(self, id: str, provider: str, user_id: str): ...
    def link_user_account(self, user_id: str, body: dict[str, Incomplete]) -> _list[dict[str, Incomplete]]:
        """Link user accounts.

        Links the account specified in the body (secondary account) to the
        account specified by the id param of the URL (primary account).

        Args:
            id (str): The user_id of the primary identity where you are linking
                the secondary account to.

            body (dict): the attributes to send as part of this request.

        See: https://auth0.com/docs/api/v2#!/Users/post_identities
        """

    async def link_user_account_async(self, user_id: str, body: dict[str, Incomplete]) -> _list[dict[str, Incomplete]]: ...
    def regenerate_recovery_code(self, user_id: str) -> dict[str, Incomplete]:
        """Removes the current recovery token, generates and returns a new one

        Args:
            user_id (str):  The user_id of the user identity.

        See: https://auth0.com/docs/api/management/v2#!/Users/post_recovery_code_regeneration
        """

    async def regenerate_recovery_code_async(self, user_id: str) -> dict[str, Incomplete]: ...
    def get_guardian_enrollments(self, user_id: str) -> dict[str, Incomplete]:
        """Retrieve the first confirmed Guardian enrollment for a user.

        Args:
            user_id (str):  The user_id of the user to retrieve.

        See: https://auth0.com/docs/api/management/v2#!/Users/get_enrollments
        """

    async def get_guardian_enrollments_async(self, user_id: str) -> dict[str, Incomplete]: ...
    def get_log_events(
        self, user_id: str, page: int = 0, per_page: int = 50, sort: str | None = None, include_totals: bool = False
    ) -> dict[str, Incomplete]:
        """Retrieve every log event for a specific user id.

        Args:
            user_id (str):  The user_id of the logs to retrieve.

            page (int, optional): The result's page number (zero based). By default,
                retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
                retrieves 50 results per page.

            sort (str, optional):  The field to use for sorting. Use field:order
                where order is 1 for ascending and -1 for descending.
                For example date:-1
                When not set, the default value is up to the server.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to False.

        See: https://auth0.com/docs/api/management/v2#!/Users/get_logs_by_user
        """

    async def get_log_events_async(
        self, user_id: str, page: int = 0, per_page: int = 50, sort: str | None = None, include_totals: bool = False
    ) -> dict[str, Incomplete]: ...
    def invalidate_remembered_browsers(self, user_id: str) -> dict[str, Incomplete]:
        """Invalidate all remembered browsers across all authentication factors for a user.

        Args:
            user_id (str):  The user_id to invalidate remembered browsers for.

        See: https://auth0.com/docs/api/management/v2#!/Users/post_invalidate_remember_browser
        """

    async def invalidate_remembered_browsers_async(self, user_id: str) -> dict[str, Incomplete]: ...
    def get_authentication_methods(self, user_id: str) -> dict[str, Incomplete]:
        """Gets a list of authentication methods

        Args:
            user_id (str):  The user_id to get a list of authentication methods for.

        See: https://auth0.com/docs/api/management/v2#!/Users/get_authentication_methods
        """

    async def get_authentication_methods_async(self, user_id: str) -> dict[str, Incomplete]: ...
    def get_authentication_method_by_id(self, user_id: str, authentication_method_id: str) -> dict[str, Incomplete]:
        """Gets an authentication method by ID.

        Args:
            user_id (str):  The user_id to get an authentication method by ID for.
            authentication_method_id (str):  The authentication_method_id to get an authentication method by ID for.

        See: https://auth0.com/docs/api/management/v2#!/Users/get_authentication_methods_by_authentication_method_id
        """

    async def get_authentication_method_by_id_async(
        self, user_id: str, authentication_method_id: str
    ) -> dict[str, Incomplete]: ...
    def create_authentication_method(self, user_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Creates an authentication method for a given user.

        Args:
            user_id (str):  The user_id to create an authentication method for a given user.
            body (dict): the request body to create an authentication method for a given user.

        See: https://auth0.com/docs/api/management/v2#!/Users/post_authentication_methods
        """

    async def create_authentication_method_async(self, user_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def update_authentication_methods(self, user_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Updates all authentication methods for a user by replacing them with the given ones.

        Args:
            user_id (str):  The user_id to update all authentication methods for.
            body (dict): the request body to update all authentication methods with.

        See: https://auth0.com/docs/api/management/v2#!/Users/put_authentication_methods
        """

    async def update_authentication_methods_async(self, user_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def update_authentication_method_by_id(
        self, user_id: str, authentication_method_id: str, body: dict[str, Incomplete]
    ) -> dict[str, Incomplete]:
        """Updates an authentication method.

        Args:
            user_id (str):  The user_id to update an authentication method.
            authentication_method_id (str):  The authentication_method_id to update an authentication method for.
            body (dict): the request body to update an authentication method.

        See: https://auth0.com/docs/api/management/v2#!/Users/patch_authentication_methods_by_authentication_method_id
        """

    async def update_authentication_method_by_id_async(
        self, user_id: str, authentication_method_id: str, body: dict[str, Incomplete]
    ) -> dict[str, Incomplete]: ...
    def delete_authentication_methods(self, user_id: str):
        """Deletes all authentication methods for the given user.

        Args:
            user_id (str):  The user_id to delete all authentication methods for the given user for.

        See: https://auth0.com/docs/api/management/v2#!/Users/delete_authentication_methods
        """

    async def delete_authentication_methods_async(self, user_id: str): ...
    def delete_authentication_method_by_id(self, user_id: str, authentication_method_id: str):
        """Deletes an authentication method by ID.

        Args:
            user_id (str):  The user_id to delete an authentication method by ID for.
            authentication_method_id (str):  The authentication_method_id to delete an authentication method by ID for.

        See: https://auth0.com/docs/api/management/v2#!/Users/delete_authentication_methods_by_authentication_method_id
        """

    async def delete_authentication_method_by_id_async(self, user_id: str, authentication_method_id: str): ...
    def list_tokensets(self, id: str, page: int = 0, per_page: int = 25, include_totals: bool = True):
        """List all the tokenset(s) associated to the user.

        Args:
            id (str): The user's id.

            page (int, optional): The result's page number (zero based). By default,
               retrieves the first page of results.

            per_page (int, optional): The amount of entries per page. By default,
               retrieves 25 results per page.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to True.

        See https://auth0.com/docs/api/management/v2#!/Users/get_tokensets
        """

    def delete_tokenset_by_id(self, user_id: str, tokenset_id: str):
        """Deletes an tokenset by ID.

        Args:
            user_id (str):  The user_id to delete an authentication method by ID for.
            tokenset_id (str):  The tokenset_id to delete an tokenset by ID for.

        See: https://auth0.com/docs/api/management/v2#!/Users/delete_tokenset_by_id
        """
