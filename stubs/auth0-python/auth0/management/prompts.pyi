from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Prompts:
    """Auth0 prompts endpoints

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
    def get(self) -> dict[str, Incomplete]:
        """Retrieves prompts settings.

        See: https://auth0.com/docs/api/management/v2#!/Prompts/get_prompts
        """

    async def get_async(self) -> dict[str, Incomplete]: ...
    def update(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Updates prompts settings.

        See: https://auth0.com/docs/api/management/v2#!/Prompts/patch_prompts
        """

    async def update_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_custom_text(self, prompt: str, language: str):
        """Retrieves custom text for a prompt in a specific language.

        Args:
            prompt (str): Name of the prompt.

            language (str): Language to update.

        See: https://auth0.com/docs/api/management/v2#!/Prompts/get_custom_text_by_language
        """

    async def get_custom_text_async(self, prompt: str, language: str): ...
    def update_custom_text(self, prompt: str, language: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Updates custom text for a prompt in a specific language.

        Args:
            prompt (str): Name of the prompt.

            language (str): Language to update.

            body (dict): An object containing custom dictionaries for a group of screens.

        See: https://auth0.com/docs/api/management/v2#!/Prompts/put_custom_text_by_language
        """

    async def update_custom_text_async(
        self, prompt: str, language: str, body: dict[str, Incomplete]
    ) -> dict[str, Incomplete]: ...
