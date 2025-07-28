from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class EmailTemplates:
    """Auth0 email templates endpoints

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
    def create(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Create a new email template.

        Args:
           body (dict): Attributes for the new email template.

        See: https://auth0.com/docs/api/management/v2#!/Email_Templates/post_email_templates
        """

    async def create_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
    def get(self, template_name: str) -> dict[str, Incomplete]:
        """Retrieves an email template by its name.

        Args:
           template_name (str): Name of the email template to get.
              Must be one of: 'verify_email', 'reset_email', 'welcome_email',
              'blocked_account', 'stolen_credentials', 'enrollment_email',
              'change_password', 'password_reset', 'mfa_oob_code'.

        See: https://auth0.com/docs/api/management/v2#!/Email_Templates/get_email_templates_by_templateName
        """

    async def get_async(self, template_name: str) -> dict[str, Incomplete]: ...
    def update(self, template_name: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Update an existing email template.

        Args:
           template_name (str): Name of the email template to update.
              Must be one of: 'verify_email', 'reset_email', 'welcome_email',
              'blocked_account', 'stolen_credentials', 'enrollment_email',
              'change_password', 'password_reset', 'mfa_oob_code'.

           body (dict): Attributes to update on the email template.

        See: https://auth0.com/docs/api/management/v2#!/Email_Templates/patch_email_templates_by_templateName
        """

    async def update_async(self, template_name: str, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
