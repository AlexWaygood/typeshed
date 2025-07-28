from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class UserBlocks:
    """Auth0 user blocks endpoints

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
    def get_by_identifier(self, identifier: str) -> dict[str, Incomplete]:
        """Gets blocks by identifier

        Args:
           identifier (str): Should be any of: username, phone_number, email.

        See: https://auth0.com/docs/api/management/v2#!/User_Blocks/get_user_blocks
        """

    async def get_by_identifier_async(self, identifier: str) -> dict[str, Incomplete]: ...
    def unblock_by_identifier(self, identifier: dict[str, Incomplete]):
        """Unblocks by identifier

        Args:
           identifier (str): Should be any of: username, phone_number, email.

        See: https://auth0.com/docs/api/management/v2#!/User_Blocks/delete_user_blocks
        """

    async def unblock_by_identifier_async(self, identifier: dict[str, Incomplete]): ...
    def get(self, id: str) -> dict[str, Incomplete]:
        """Get a user's blocks

        Args:
           id (str): The user_id of the user to retrieve.

        See: https://auth0.com/docs/api/management/v2#!/User_Blocks/get_user_blocks_by_id
        """

    async def get_async(self, id: str) -> dict[str, Incomplete]: ...
    def unblock(self, id: str):
        """Unblock a user

        Args:
           id (str): The user_id of the user to update.

        See: https://auth0.com/docs/api/management/v2#!/User_Blocks/delete_user_blocks_by_id
        """

    async def unblock_async(self, id: str): ...
