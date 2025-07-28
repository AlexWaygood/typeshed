from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Actions:
    """Auth0 Actions endpoints

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

        rest_options (RestClientOptions, optional): Pass an instance of
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
    def get_actions(
        self,
        trigger_id: str | None = None,
        action_name: str | None = None,
        deployed: bool | None = None,
        installed: bool = False,
        page: int | None = None,
        per_page: int | None = None,
    ):
        """Get all actions.

        Args:
           trigger_id (str, optional): Filter the results to only actions associated
                 with this trigger ID.

           action_name (str, optional): Filter the results to only actions with this name.

           deployed (bool, optional): True to filter the results to only deployed actions.
                Defaults to False.

           installed (bool, optional): True to filter the results to only installed actions.
                Defaults to False.

           page (int, optional): The result's page number (zero based). When not set,
                the default value is up to the server.

           per_page (int, optional): The amount of entries per page. When not set,
                the default value is up to the server.

        See: https://auth0.com/docs/api/management/v2#!/Actions/get_actions
        """

    async def get_actions_async(
        self,
        trigger_id: str | None = None,
        action_name: str | None = None,
        deployed: bool | None = None,
        installed: bool = False,
        page: int | None = None,
        per_page: int | None = None,
    ): ...
    def create_action(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create a new action.

        Args:
           body (dict): Attributes for the new action.

        See: https://auth0.com/docs/api/management/v2#!/Actions/post_action
        """

    async def create_action_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def update_action(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Updates an action.

        Args:
           id (str): the ID of the action.

           body (dict): Attributes to modify.

        See: https://auth0.com/docs/api/management/v2#!/Actions/patch_action
        """

    async def update_action_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_action(self, id: str) -> dict[str, Incomplete]:
        """Retrieves an action by its ID.

        Args:
           id (str): Id of action to retrieve.

        See: https://auth0.com/docs/api/management/v2#!/Actions/get_action
        """

    async def get_action_async(self, id: str) -> dict[str, Incomplete]: ...
    def delete_action(self, id: str, force: bool = False):
        """Deletes an action and all of its associated versions.

        Args:
           id (str): ID of the action to delete.

           force (bool, optional): True to force action deletion detaching bindings,
               False otherwise. Defaults to False.

        See: https://auth0.com/docs/api/management/v2#!/Actions/delete_action
        """

    async def delete_action_async(self, id: str, force: bool = False): ...
    def get_triggers(self) -> dict[str, Incomplete]:
        """Retrieve the set of triggers currently available within actions.

        See: https://auth0.com/docs/api/management/v2#!/Actions/get_triggers
        """

    async def get_triggers_async(self) -> dict[str, Incomplete]: ...
    def get_execution(self, id: str) -> dict[str, Incomplete]:
        """Get information about a specific execution of a trigger.

        Args:
           id (str): The ID of the execution to retrieve.

        See: https://auth0.com/docs/api/management/v2#!/Actions/get_execution
        """

    async def get_execution_async(self, id: str) -> dict[str, Incomplete]: ...
    def get_action_versions(self, id: str, page: int | None = None, per_page: int | None = None) -> dict[str, Incomplete]:
        """Get all of an action's versions.

        Args:
           id (str): The ID of the action.

           page (int, optional): The result's page number (zero based). When not set,
                the default value is up to the server.

           per_page (int, optional): The amount of entries per page. When not set,
                the default value is up to the server.

        See: https://auth0.com/docs/api/management/v2#!/Actions/get_action_versions
        """

    async def get_action_versions_async(
        self, id: str, page: int | None = None, per_page: int | None = None
    ) -> dict[str, Incomplete]: ...
    def get_trigger_bindings(self, id: str, page: int | None = None, per_page: int | None = None) -> dict[str, Incomplete]:
        """Get the actions that are bound to a trigger.

        Args:
           id (str): The trigger ID.

           page (int, optional): The result's page number (zero based). When not set,
                the default value is up to the server.

           per_page (int, optional): The amount of entries per page. When not set,
                the default value is up to the server.

        See: https://auth0.com/docs/api/management/v2#!/Actions/get_bindings
        """

    async def get_trigger_bindings_async(
        self, id: str, page: int | None = None, per_page: int | None = None
    ) -> dict[str, Incomplete]: ...
    def get_action_version(self, action_id: str, version_id: str) -> dict[str, Incomplete]:
        """Retrieve a specific version of an action.

        Args:
           action_id (str): The ID of the action.

           version_id (str): The ID of the version to retrieve.

        See: https://auth0.com/docs/api/management/v2#!/Actions/get_action_version
        """

    async def get_action_version_async(self, action_id: str, version_id: str) -> dict[str, Incomplete]: ...
    def deploy_action(self, id: str) -> dict[str, Incomplete]:
        """Deploy an action.

        Args:
           id (str): The ID of the action to deploy.

        See: https://auth0.com/docs/api/management/v2#!/Actions/post_deploy_action
        """

    async def deploy_action_async(self, id: str) -> dict[str, Incomplete]: ...
    def rollback_action_version(self, action_id: str, version_id: str) -> dict[str, Incomplete]:
        """Roll back to a previous version of an action.

        Args:
           action_id (str): The ID of the action.

           version_id (str): The ID of the version.

        See: https://auth0.com/docs/api/management/v2#!/Actions/post_deploy_draft_version
        """

    async def rollback_action_version_async(self, action_id: str, version_id: str) -> dict[str, Incomplete]: ...
    def update_trigger_bindings(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update a trigger's bindings.

        Args:
           id (str): The ID of the trigger to update.

           body (dict): Attributes for the updated trigger binding.

        See: https://auth0.com/docs/api/management/v2#!/Actions/patch_bindings
        """

    async def update_trigger_bindings_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
