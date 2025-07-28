from _typeshed import Incomplete
from builtins import list as _list

from ..rest import RestClientOptions
from ..types import TimeoutType

class LogStreams:
    """Auth0 log streams endpoints

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
    def list(self) -> _list[dict[str, Incomplete]]:
        """Search log events.

        Args:
        See: https://auth0.com/docs/api/management/v2/#!/Log_Streams/get_log_streams
        """

    async def list_async(self) -> _list[dict[str, Incomplete]]: ...
    def get(self, id: str) -> dict[str, Incomplete]:
        """Retrieves the data related to the log stream entry identified by id.

        Args:
            id (str): The id of the log stream to retrieve.

        See: https://auth0.com/docs/api/management/v2/#!/Log_Streams/get_log_streams_by_id
        """

    async def get_async(self, id: str) -> dict[str, Incomplete]: ...
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Creates a new log stream.

        Args:
            body (dict): the attributes for the role to create.

        See: https://auth0.com/docs/api/management/v2/#!/Log_Streams/post_log_streams
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete(self, id: str) -> dict[str, Incomplete]:
        """Delete a log stream.

        Args:
            id (str): The id of the log ste to delete.

        See: https://auth0.com/docs/api/management/v2/#!/Log_Streams/delete_log_streams_by_id
        """

    async def delete_async(self, id: str) -> dict[str, Incomplete]: ...
    def update(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update a log stream with the attributes passed in 'body'

        Args:
            id (str): The id of the log stream to update.

            body (dict): the attributes to update on the log stream.

        See: https://auth0.com/docs/api/management/v2/#!/Log_Streams/patch_log_streams_by_id
        """

    async def update_async(self, id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
