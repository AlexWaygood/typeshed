from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Organizations:
    """Auth0 organizations endpoints

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
    def all_organizations(
        self,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = True,
        from_param: str | None = None,
        take: int | None = None,
    ) -> dict[str, Incomplete]:
        """Retrieves a list of all the organizations.

        Args:
            page (int): The result's page number (zero based). When not set,
                the default value is up to the server.

            per_page (int, optional): The amount of entries per page. When not set,
                the default value is up to the server.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to True.

            from_param (str, optional): Checkpoint Id from which to begin retrieving results.
                You can limit the number of entries using the take parameter.

            take (int, optional): The total amount of entries to retrieve when
                using the from parameter. When not set, the default value is up to the server.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/get_organizations
        """

    async def all_organizations_async(
        self,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = True,
        from_param: str | None = None,
        take: int | None = None,
    ) -> dict[str, Incomplete]: ...
    def get_organization_by_name(self, name: str | None = None) -> dict[str, Incomplete]:
        """Retrieves an organization given its name.

        Args:
           name (str): The name of the organization to retrieve.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/get_name_by_name
        """

    async def get_organization_by_name_async(self, name: str | None = None) -> dict[str, Incomplete]: ...
    def get_organization(self, id: str) -> dict[str, Incomplete]:
        """Retrieves an organization by its ID.

        Args:
           id (str): Id of organization to retrieve.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/get_organizations_by_id
        """

    async def get_organization_async(self, id: str) -> dict[str, Incomplete]: ...
    def create_organization(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create a new organization.

        Args:
           body (dict): Attributes for the new organization.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/post_organizations
        """

    async def create_organization_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def update_organization(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Modifies an organization.

        Args:
           id (str): the ID of the organization.

           body (dict): Attributes to modify.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/patch_organizations_by_id
        """

    async def update_organization_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete_organization(self, id: str):
        """Deletes an organization and all its related assets.

        Args:
           id (str): Id of organization to delete.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/delete_organizations_by_id
        """

    async def delete_organization_async(self, id: str): ...
    def all_organization_connections(
        self, id: str, page: int | None = None, per_page: int | None = None
    ) -> list[dict[str, Incomplete]]:
        """Retrieves a list of all the organization connections.

        Args:
           id (str): the ID of the organization.

           page (int): The result's page number (zero based). When not set,
              the default value is up to the server.

           per_page (int, optional): The amount of entries per page. When not set,
              the default value is up to the server.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/get_enabled_connections
        """

    async def all_organization_connections_async(
        self, id: str, page: int | None = None, per_page: int | None = None
    ) -> list[dict[str, Incomplete]]: ...
    def get_organization_connection(self, id: str, connection_id: str) -> dict[str, Incomplete]:
        """Retrieves an organization connection by its ID.

        Args:
           id (str): the ID of the organization.

           connection_id (str): the ID of the connection.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/get_enabled_connections_by_connectionId
        """

    async def get_organization_connection_async(self, id: str, connection_id: str) -> dict[str, Incomplete]: ...
    def create_organization_connection(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Adds a connection to an organization.

        Args:
           id (str): the ID of the organization.

           body (dict): Attributes for the connection to add.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/post_enabled_connections
        """

    async def create_organization_connection_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def update_organization_connection(self, id: str, connection_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Modifies an organization.

        Args:
           id (str): the ID of the organization.

           connection_id (str): the ID of the connection to update.

           body (dict): Attributes to modify.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/patch_enabled_connections_by_connectionId
        """

    async def update_organization_connection_async(
        self, id: str, connection_id: str, body: dict[str, Incomplete]
    ) -> dict[str, Incomplete]: ...
    def delete_organization_connection(self, id: str, connection_id: str):
        """Deletes a connection from the given organization.

        Args:
           id (str): Id of organization.

           connection_id (str): the ID of the connection to delete.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/delete_enabled_connections_by_connectionId
        """

    async def delete_organization_connection_async(self, id: str, connection_id: str): ...
    def all_organization_members(
        self,
        id: str,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = True,
        from_param: str | None = None,
        take: int | None = None,
        fields: list[str] | None = None,
        include_fields: bool = True,
    ) -> dict[str, Incomplete]:
        """Retrieves a list of all the organization members.

        Member roles are not sent by default. Use `fields=roles` to retrieve the roles assigned to each listed member.
        To use this parameter, you must include the `read:organization_member_roles scope` in the token.

        Args:
            id (str): the ID of the organization.

            page (int): The result's page number (zero based). When not set,
                the default value is up to the server.

            per_page (int, optional): The amount of entries per page. When not set,
                the default value is up to the server.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to True.

            from_param (str, optional): Checkpoint Id from which to begin retrieving results.
                You can limit the number of entries using the take parameter.

            take (int, optional): The total amount of entries to retrieve when
                using the from parameter. When not set, the default value is up to the server.

            fields (list of str, optional): A list of fields to include or
              exclude from the result (depending on include_fields). If fields is left blank,
              all fields (except roles) are returned.

            include_fields (bool, optional): True if the fields specified are
              to be included in the result, False otherwise. Defaults to True.

        See: https://auth0.com/docs/api/management/v2/organizations/get-members
        """

    async def all_organization_members_async(
        self,
        id: str,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = True,
        from_param: str | None = None,
        take: int | None = None,
        fields: list[str] | None = None,
        include_fields: bool = True,
    ) -> dict[str, Incomplete]: ...
    def create_organization_members(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Adds members to an organization.

        Args:
           id (str): the ID of the organization.

           body (dict): Attributes from the members to add.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/post_members
        """

    async def create_organization_members_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete_organization_members(self, id: str, body: dict[str, Incomplete]):
        """Deletes members from the given organization.

        Args:
           id (str): Id of organization.

           body (dict): Attributes from the members to delete

        See: https://auth0.com/docs/api/management/v2#!/Organizations/delete_members
        """

    async def delete_organization_members_async(self, id: str, body: dict[str, Incomplete]): ...
    def all_organization_member_roles(
        self, id: str, user_id: str, page: int | None = None, per_page: int | None = None, include_totals: bool = False
    ) -> list[dict[str, Incomplete]]:
        """Retrieves a list of all the roles from the given organization member.

        Args:
           id (str): the ID of the organization.

           user_id (str): the ID of the user member of the organization.

           page (int): The result's page number (zero based). When not set,
              the default value is up to the server.

           per_page (int, optional): The amount of entries per page. When not set,
              the default value is up to the server.

           include_totals (bool, optional): True if the query summary is
              to be included in the result, False otherwise. Defaults to False.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/get_organization_member_roles
        """

    async def all_organization_member_roles_async(
        self, id: str, user_id: str, page: int | None = None, per_page: int | None = None, include_totals: bool = False
    ) -> list[dict[str, Incomplete]]: ...
    def create_organization_member_roles(self, id: str, user_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Adds roles to a member of an organization.

        Args:
           id (str): the ID of the organization.

           user_id (str): the ID of the user member of the organization.

           body (dict): Attributes from the members to add.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/post_organization_member_roles
        """

    async def create_organization_member_roles_async(
        self, id: str, user_id: str, body: dict[str, Incomplete]
    ) -> dict[str, Incomplete]: ...
    def delete_organization_member_roles(self, id: str, user_id: str, body: dict[str, Incomplete]):
        """Deletes roles from a member of an organization.

        Args:
           id (str): Id of organization.

           user_id (str): the ID of the user member of the organization.

           body (dict): Attributes from the members to delete

        See: https://auth0.com/docs/api/management/v2#!/Organizations/delete_organization_member_roles
        """

    async def delete_organization_member_roles_async(self, id: str, user_id: str, body: dict[str, Incomplete]): ...
    def all_organization_invitations(
        self, id: str, page: int | None = None, per_page: int | None = None, include_totals: bool = False
    ) -> dict[str, Incomplete]:
        """Retrieves a list of all the organization invitations.

        Args:
           id (str): the ID of the organization.

           page (int): The result's page number (zero based). When not set,
              the default value is up to the server.

           per_page (int, optional): The amount of entries per page. When not set,
              the default value is up to the server.

           include_totals (bool, optional): True if the query summary is
              to be included in the result, False otherwise. Defaults to False.
              NOTE: returns start and limit, total count is not yet supported

        See: https://auth0.com/docs/api/management/v2#!/Organizations/get_invitations
        """

    async def all_organization_invitations_async(
        self, id: str, page: int | None = None, per_page: int | None = None, include_totals: bool = False
    ) -> dict[str, Incomplete]: ...
    def get_organization_invitation(self, id: str, invitaton_id: str) -> dict[str, Incomplete]:
        """Retrieves an organization invitation by its ID.

        Args:
           id (str): the ID of the organization.

           invitaton_id (str): the ID of the invitation.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/get_invitations_by_invitation_id
        """

    async def get_organization_invitation_async(self, id: str, invitaton_id: str) -> dict[str, Incomplete]: ...
    def create_organization_invitation(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create an invitation to an organization.

        Args:
           id (str): the ID of the organization.

           body (dict): Attributes for the invitation to create.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/post_invitations
        """

    async def create_organization_invitation_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete_organization_invitation(self, id: str, invitation_id: str):
        """Deletes an invitation from the given organization.

        Args:
           id (str): Id of organization.

           invitation_id (str): the ID of the invitation to delete.

        See: https://auth0.com/docs/api/management/v2#!/Organizations/delete_invitations_by_invitation_id
        """

    async def delete_organization_invitation_async(self, id: str, invitation_id: str): ...
    def get_client_grants(
        self,
        id: str,
        audience: str | None = None,
        client_id: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
    ) -> dict[str, Incomplete]:
        """Get client grants associated to an organization.

        Args:
            id (str): Id of organization.

            audience (str, optional): URL encoded audience of a Resource Server
                to filter.

            client_id (string, optional): The id of a client to filter.

            page (int, optional): The result's page number (zero based). When not set,
                the default value is up to the server.

            per_page (int, optional): The amount of entries per page. When not set,
                the default value is up to the server.

            include_totals (bool, optional): True if the query summary is
                to be included in the result, False otherwise. Defaults to False.
        """

    async def get_client_grants_async(
        self,
        id: str,
        audience: str | None = None,
        client_id: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_totals: bool = False,
    ) -> dict[str, Incomplete]: ...
    def add_client_grant(self, id: str, grant_id: str) -> dict[str, Incomplete]:
        """Associate a client grant with an organization.

        Args:
           id (str): the ID of the organization.

           grant_id (string) A Client Grant ID to add to the organization.
        """

    async def add_client_grant_async(self, id: str, grant_id: str) -> dict[str, Incomplete]: ...
    def delete_client_grant(self, id: str, grant_id: str) -> dict[str, Incomplete]:
        """Remove a client grant from an organization.

        Args:
           id (str): the ID of the organization.

           grant_id (string) A Client Grant ID to remove from the organization.
        """

    async def delete_client_grant_async(self, id: str, grant_id: str) -> dict[str, Incomplete]: ...
