from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Branding:
    """Auth0 Branding endpoints

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
        """Retrieve branding settings. Requires "read:branding" scope.

        See: https://auth0.com/docs/api/management/v2#!/Branding/get_branding
        """

    async def get_async(self) -> dict[str, Incomplete]: ...
    def update(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update branding settings. Requires "update:branding" scope.

        Args:
            body (dict): Attributes for the updated trigger binding.

        See: https://auth0.com/docs/api/management/v2#!/Branding/patch_branding
        """

    async def update_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_template_universal_login(self) -> dict[str, Incomplete]:
        """Get template for New Universal Login Experience. Requires "read:branding" scope.

        See: https://auth0.com/docs/api/management/v2#!/Branding/get_universal_login
        """

    async def get_template_universal_login_async(self) -> dict[str, Incomplete]: ...
    def delete_template_universal_login(self):
        """Delete template for New Universal Login Experience. Requires "delete:branding" scope.

        See: https://auth0.com/docs/api/management/v2#!/Branding/delete_universal_login
        """

    async def delete_template_universal_login_async(self): ...
    def update_template_universal_login(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update template for New Universal Login Experience. Requires "update:branding" scope.

        Args:
            body (str): Complete HTML content to assign to the template. See linked API documentation for example.

        See: https://auth0.com/docs/api/management/v2#!/Branding/put_universal_login
        """

    async def update_template_universal_login_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get_default_branding_theme(self) -> dict[str, Incomplete]:
        """Retrieve default branding theme.

        See: https://auth0.com/docs/api/management/v2#!/Branding/get_default_branding_theme
        """

    async def get_default_branding_theme_async(self) -> dict[str, Incomplete]: ...
    def get_branding_theme(self, theme_id: str) -> dict[str, Incomplete]:
        """Retrieve branding theme.

        Args:
            theme_id (str): The theme_id to retrieve branding theme for.

        See: https://auth0.com/docs/api/management/v2#!/Branding/get_branding_theme
        """

    async def get_branding_theme_async(self, theme_id: str) -> dict[str, Incomplete]: ...
    def delete_branding_theme(self, theme_id: str):
        """Delete branding theme.

        Args:
            theme_id (str): The theme_id to delete branding theme for.

        See: https://auth0.com/docs/api/management/v2#!/Branding/delete_branding_theme
        """

    async def delete_branding_theme_async(self, theme_id: str): ...
    def update_branding_theme(self, theme_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update branding theme.

        Args:
            theme_id (str): The theme_id to update branding theme for.
            body (dict): The attributes to set on the theme.

        See: https://auth0.com/docs/api/management/v2#!/Branding/patch_branding_theme
        """

    async def update_branding_theme_async(self, theme_id: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def create_branding_theme(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create branding theme.

        Args:
            body (dict): The attributes to set on the theme.

        See: https://auth0.com/docs/api/management/v2#!/Branding/post_branding_theme
        """

    async def create_branding_theme_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
