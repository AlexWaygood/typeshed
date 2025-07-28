from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Emails:
    """Auth0 email endpoints

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
    def get(self, fields: list[str] | None = None, include_fields: bool = True) -> dict[str, Incomplete]:
        """Get the email provider.

        Args:
            fields (list of str, optional): A list of fields to include or
                exclude from the result (depending on include_fields). Leave empty to
                retrieve all fields.

            include_fields (bool, optional): True if the fields specified are
                to be included in the result, False otherwise. Defaults to True.

        See: https://auth0.com/docs/api/management/v2#!/Emails/get_provider
        """

    async def get_async(self, fields: list[str] | None = None, include_fields: bool = True) -> dict[str, Incomplete]: ...
    def config(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Configure the email provider.

        Args:
            body (dict): attributes of the created email provider.

        See: https://auth0.com/docs/api/v2#!/Emails/post_provider
        """

    async def config_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def delete(self):
        """Delete the email provider. (USE WITH CAUTION)

        See: https://auth0.com/docs/api/management/v2#!/Emails/delete_provider
        """

    async def delete_async(self): ...
    def update(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update the email provider.

        Args:
            body (dict): attributes to update on the email provider

        See: https://auth0.com/docs/api/v2#!/Emails/patch_provider
        """

    async def update_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
